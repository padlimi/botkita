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
        "/help - Bantuan\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 **KlikIndomaret Bot Help**

**Fitur Utama:**
1. `/login` - Login dengan akun KlikIndomaret
2. `/search <keyword>` - Cari produk (contoh: /search beras)
3. `/cart` - Lihat isi keranjang
4. `/orders` - Riwayat pesanan
5. `/wishlist` - Daftar favorit
6. `/profile` - Info profil
7. `/logout` - Keluar akun

**Contoh Penggunaan:**
- /search beras
- /cart
- /orders

Butuh bantuan? Hubungi @support_klikindomaret
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    text = update.message.text
    await update.message.reply_text(f"Pesan Anda: {text}\n\nGunakan perintah /help untuk bantuan")

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()