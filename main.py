import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token dari environment variable
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# ==================== COMMAND HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 👋\n\n"
        "Selamat datang di KlikIndomaret Bot! 🤖\n\n"
        "Perintah yang tersedia:\n"
        "/login - Login ke akun KlikIndomaret\n"
        "/search - Cari produk\n"
        "/cart - Lihat keranjang belanja\n"
        "/orders - Lihat pesanan\n"
        "/wishlist - Daftar favorit\n"
        "/profile - Info profil\n"
        "/help - Bantuan\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 KlikIndomaret Bot Help\n\n"
        "Fitur Utama:\n"
        "1. /login - Login dengan akun KlikIndomaret\n"
        "2. /search <keyword> - Cari produk (contoh: /search beras)\n"
        "3. /cart - Lihat isi keranjang\n"
        "4. /orders - Riwayat pesanan\n"
        "5. /wishlist - Daftar favorit\n"
        "6. /profile - Info profil\n"
        "7. /logout - Keluar akun\n\n"
        "Contoh Penggunaan:\n"
        "- /search beras\n"
        "- /cart\n"
        "- /orders\n\n"
        "Butuh bantuan? Hubungi @support_klikindomaret"
    )
    await update.message.reply_text(help_text)

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /login command"""
    await update.message.reply_text(
        "🔐 Login KlikIndomaret\n\n"
        "Silakan pilih metode login:\n"
        "1️⃣ Email + Password\n"
        "2️⃣ No. HP + OTP\n\n"
        "Kirim: login email atau login phone"
    )

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /search command"""
    if not context.args:
        await update.message.reply_text(
            "🔍 Search Produk\n\n"
            "Gunakan: /search <keyword>\n"
            "Contoh: /search beras"
        )
        return
    
    keyword = ' '.join(context.args)
    await update.message.reply_text(
        f"🔍 Mencari produk: {keyword}\n\n"
        "⏳ Sedang mencari...\n"
        "(Fitur ini sedang dalam pengembangan)"
    )

async def cart_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cart command"""
    await update.message.reply_text(
        "🛒 Keranjang Belanja\n\n"
        "Keranjang Anda kosong\n\n"
        "Gunakan /search untuk mencari produk"
    )

async def orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /orders command"""
    await update.message.reply_text(
        "📦 Riwayat Pesanan\n\n"
        "Anda belum memiliki pesanan\n\n"
        "Login terlebih dahulu dengan /login"
    )

async def wishlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /wishlist command"""
    await update.message.reply_text(
        "❤️ Daftar Favorit\n\n"
        "Daftar favorit Anda kosong\n\n"
        "Gunakan /search untuk mencari produk"
    )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /profile command"""
    user = update.effective_user
    await update.message.reply_text(
        f"👤 Profil\n\n"
        f"Nama: {user.first_name}\n"
        f"Username: @{user.username}\n"
        f"ID: {user.id}\n\n"
        "Status: Belum login\n\n"
        "Gunakan /login untuk login ke KlikIndomaret"
    )

async def logout_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /logout command"""
    await update.message.reply_text(
        "👋 Anda telah logout\n\n"
        "Gunakan /login untuk login kembali"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    text = update.message.text
    await update.message.reply_text(
        f"Pesan: {text}\n\n"
        "Gunakan perintah /help untuk bantuan"
    )

# ==================== MAIN FUNCTION ====================

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("login", login_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("cart", cart_command))
    application.add_handler(CommandHandler("orders", orders_command))
    application.add_handler(CommandHandler("wishlist", wishlist_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("logout", logout_command))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
