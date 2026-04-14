import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Muat variabel lingkungan dari file .env (untuk lokal)
load_dotenv()

# Ambil token dari environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("TELEGRAM_TOKEN dan GEMINI_API_KEY harus diatur di environment variables.")

# Konfigurasi Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Setup model Gemini (gunakan model yang sesuai, misal "gemini-1.5-flash")
model = genai.GenerativeModel("gemini-1.5-flash")

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Chat history sederhana (dalam memori, tidak permanen)
# Format: {user_id: [{"role": "user", "parts": ["teks"]}, ...]}
# Untuk produksi, lebih baik pakai database.
chat_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan sambutan saat perintah /start dikirim."""
    await update.message.reply_text(
        "👋 Halo! Saya bot asisten AI dengan Gemini.\n"
        "Silakan kirim pesan teks apa saja, saya akan membalas dengan jawaban dari Gemini.\n"
        "Gunakan /reset untuk menghapus riwayat percakapan.\n"
        "Gunakan /help untuk bantuan."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan bantuan."""
    await update.message.reply_text(
        "🤖 *Bot Gemini Telegram*\n\n"
        "Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Tampilkan bantuan ini\n"
        "/reset - Hapus riwayat percakapan\n\n"
        "Kirim pesan teks apa saja untuk mendapatkan respons dari Google Gemini AI.",
        parse_mode="Markdown"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menghapus riwayat percakapan user."""
    user_id = update.effective_user.id
    if user_id in chat_sessions:
        del chat_sessions[user_id]
    await update.message.reply_text("✅ Riwayat percakapan telah dihapus.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menangani pesan teks dari user dan membalas dengan respons Gemini."""
    user_id = update.effective_user.id
    user_message = update.message.text

    # Kirim status "mengetik" agar user tahu bot sedang memproses
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Ambil atau buat history untuk user ini
        if user_id not in chat_sessions:
            chat_sessions[user_id] = []

        # Bangun percakapan untuk Gemini
        # Format chat history untuk Gemini
        # Kita perlu mengubah history kita menjadi format yang dimengerti GenerativeModel
        # Gemini chat session lebih mudah dengan start_chat()
        # Kita simpan objek chat di context atau dictionary?
        # Alternatif: gunakan model.start_chat() dan simpan history secara manual.

        # Pendekatan sederhana: buat chat baru setiap kali dengan history yang sudah ada
        # Tapi untuk menjaga konteks, kita gunakan send_message dengan chat history.
        chat = model.start_chat(history=chat_sessions[user_id])
        response = chat.send_message(user_message)

        # Tambahkan pertanyaan user dan respons model ke history
        chat_sessions[user_id].append({"role": "user", "parts": [user_message]})
        chat_sessions[user_id].append({"role": "model", "parts": [response.text]})

        # Balas ke user
        await update.message.reply_text(response.text)

    except Exception as e:
        logger.error(f"Error saat memproses pesan dari user {user_id}: {e}")
        await update.message.reply_text(
            "❌ Maaf, terjadi kesalahan saat memproses permintaan Anda. Silakan coba lagi nanti."
        )

def main() -> None:
    """Fungsi utama untuk menjalankan bot."""
    # Buat aplikasi bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Daftarkan handler perintah
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset))

    # Daftarkan handler untuk pesan teks (hanya teks, bukan perintah)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Mulai bot (polling)
    logger.info("Bot dimulai...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
