import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
    ConversationHandler, CallbackQueryHandler
)
from sqlalchemy.orm import Session
from database import get_db, User, SessionLocal
from utils.klik_indomaret import validate_email, validate_phone, hash_password
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Conversation states
EMAIL_INPUT, PASSWORD_INPUT, PHONE_INPUT, OTP_INPUT, OTP_VERIFY = range(5)

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start login process"""
    keyboard = [
        ["📧 Email + Password"],
        ["📱 Phone + OTP"],
        ["❌ Cancel"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🔐 *Login KlikIndomaret*\n\n"
        "Pilih metode login:",
        reply_markup=reply_markup
    )
    
    return 1  # Next state

async def login_method_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle login method selection"""
    choice = update.message.text
    
    if choice == "❌ Cancel":
        await update.message.reply_text(
            "Login dibatalkan",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    if choice == "📧 Email + Password":
        await update.message.reply_text(
            "📧 Masukkan email KlikIndomaret Anda:",
            reply_markup=ReplyKeyboardRemove()
        )
        return EMAIL_INPUT
    
    elif choice == "📱 Phone + OTP":
        await update.message.reply_text(
            "📱 Masukkan nomor HP Anda (format: 62812xxxx):",
            reply_markup=ReplyKeyboardRemove()
        )
        return PHONE_INPUT

async def email_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle email input"""
    email = update.message.text.strip()
    
    # Validate email format
    if not validate_email(email):
        await update.message.reply_text(
            "❌ Format email tidak valid!\n\n"
            "Contoh: user@gmail.com\n\n"
            "Coba lagi:"
        )
        return EMAIL_INPUT
    
    context.user_data['email'] = email
    
    await update.message.reply_text(
        f"✅ Email: {email}\n\n"
        "🔑 Masukkan password KlikIndomaret Anda:"
    )
    
    return PASSWORD_INPUT

async def password_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password input"""
    password = update.message.text
    email = context.user_data['email']
    
    if len(password) < 6:
        await update.message.reply_text(
            "❌ Password minimal 6 karakter!\n\n"
            "Coba lagi:"
        )
        return PASSWORD_INPUT
    
    # Simulate login ke KlikIndomaret
    # Dalam produksi, ini akan benar-benar hit KlikIndomaret API
    await update.message.reply_text("⏳ Sedang verifikasi credential...")
    
    try:
        # TODO: Implement actual KlikIndomaret API call
        # from utils.klik_indomaret import login_to_klikindomaret
        # result = await login_to_klikindomaret(email, password)
        
        # Untuk sekarang, simulasi login berhasil
        db = SessionLocal()
        
        # Cek user sudah ada atau tidak
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            user = User(
                telegram_id=update.effective_user.id,
                email=email,
                password_hash=hash_password(password),
                full_name=update.effective_user.first_name,
                is_logged_in=True,
                session_token=str(uuid.uuid4())
            )
            db.add(user)
        else:
            # Update existing user
            user.password_hash = hash_password(password)
            user.is_logged_in = True
            user.session_token = str(uuid.uuid4())
        
        db.commit()
        db.close()
        
        await update.message.reply_text(
            f"✅ Login Berhasil!\n\n"
            f"Selamat datang {email}!\n\n"
            "Gunakan perintah:\n"
            "/search - Cari produk\n"
            "/cart - Lihat keranjang\n"
            "/orders - Lihat pesanan\n"
            "/profile - Lihat profil\n"
            "/logout - Logout"
        )
        
        return ConversationHandler.END
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        await update.message.reply_text(
            "❌ Login gagal!\n\n"
            "Email atau password salah.\n\n"
            "Coba lagi: /login"
        )
        return ConversationHandler.END

async def phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone input"""
    phone = update.message.text.strip()
    
    # Validate phone format
    if not validate_phone(phone):
        await update.message.reply_text(
            "❌ Format nomor HP tidak valid!\n\n"
            "Contoh: 628123456789\n\n"
            "Coba lagi:"
        )
        return PHONE_INPUT
    
    context.user_data['phone'] = phone
    
    await update.message.reply_text(
        f"✅ No. HP: {phone}\n\n"
        "⏳ Sedang mengirim OTP..."
    )
    
    # TODO: Generate and send OTP to phone
    # from utils.klik_indomaret import send_otp
    # otp_code = generate_otp()
    # send_otp(phone, otp_code)
    
    # Untuk testing, generate OTP
    otp_code = "123456"
    context.user_data['otp_code'] = otp_code
    context.user_data['otp_attempts'] = 3
    
    await update.message.reply_text(
        f"📨 OTP sudah dikirim ke {phone}\n\n"
        "Masukkan OTP (6 digit):"
    )
    
    return OTP_INPUT

async def otp_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle OTP input"""
    otp_input_code = update.message.text.strip()
    otp_correct_code = context.user_data.get('otp_code')
    otp_attempts = context.user_data.get('otp_attempts', 3)
    
    if otp_input_code == otp_correct_code:
        phone = context.user_data['phone']
        
        try:
            db = SessionLocal()
            
            # Create new user
            user = User(
                telegram_id=update.effective_user.id,
                phone=phone,
                full_name=update.effective_user.first_name,
                is_logged_in=True,
                session_token=str(uuid.uuid4())
            )
            db.add(user)
            db.commit()
            db.close()
            
            await update.message.reply_text(
                f"✅ Login Berhasil!\n\n"
                f"Selamat datang {phone}!\n\n"
                "Gunakan perintah:\n"
                "/search - Cari produk\n"
                "/cart - Lihat keranjang\n"
                "/orders - Lihat pesanan\n"
                "/profile - Lihat profil\n"
                "/logout - Logout"
            )
            
            return ConversationHandler.END
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            await update.message.reply_text(
                "❌ Terjadi error saat login\n\n"
                "Coba lagi: /login"
            )
            return ConversationHandler.END
    
    else:
        otp_attempts -= 1
        context.user_data['otp_attempts'] = otp_attempts
        
        if otp_attempts <= 0:
            await update.message.reply_text(
                "❌ Kesempatan habis!\n\n"
                "Coba lagi: /login"
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                f"❌ OTP salah!\n\n"
                f"Kesempatan tersisa: {otp_attempts}\n\n"
                "Coba lagi:"
            )
            return OTP_INPUT

async def logout_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle logout"""
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.telegram_id == update.effective_user.id).first()
        
        if user:
            user.is_logged_in = False
            user.session_token = None
            db.commit()
        
        db.close()
        
        await update.message.reply_text(
            "👋 Anda telah logout\n\n"
            "Gunakan /login untuk login kembali"
        )
    except Exception as e:
        logger.error(f"Logout error: {e}")
        await update.message.reply_text("❌ Error saat logout")

def get_auth_handler():
    """Return conversation handler for auth"""
    return ConversationHandler(
        entry_points=[CommandHandler('login', login_command)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_method_selected)],
            EMAIL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_input)],
            PASSWORD_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_input)],
            PHONE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_input)],
            OTP_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, otp_input)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
