import os
import logging
import google.generativeai as genai
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ChatAction

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ─── Gemini setup ──────────────────────────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    system_instruction=(
        "Kamu adalah asisten AI yang cerdas, ramah, dan membantu. "
        "Jawab dalam bahasa yang sama dengan pengguna. "
        "Berikan jawaban yang jelas, akurat, dan bermanfaat."
    ),
)

# In-memory conversation history per user
chat_sessions: dict[int, any] = {}


def get_chat_session(user_id: int):
    """Get or create a Gemini chat session for a user."""
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]


# ─── Handlers ──────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"👋 Halo, <b>{user.first_name}</b>!\n\n"
        "Saya adalah bot AI yang didukung <b>Google Gemini</b>.\n"
        "Kirim pesan apa saja dan saya akan menjawabnya!\n\n"
        "📌 Perintah tersedia:\n"
        "/start – Tampilkan pesan ini\n"
        "/new   – Mulai percakapan baru\n"
        "/help  – Bantuan\n"
        "/about – Tentang bot ini"
    )


async def cmd_new(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_sessions.pop(user_id, None)
    await update.message.reply_text(
        "🔄 Percakapan baru dimulai!\nSesi sebelumnya telah dihapus."
    )


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Cara menggunakan bot ini:*\n\n"
        "• Kirim teks apa saja → saya akan menjawab\n"
        "• /new → reset percakapan (hapus memori)\n"
        "• Bot mengingat konteks percakapan dalam satu sesi\n\n"
        "💡 *Tips:* Semakin jelas pertanyaanmu, semakin baik jawabanku!",
        parse_mode="Markdown",
    )


async def cmd_about(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *Tentang Bot Ini*\n\n"
        f"• Model AI: `{GEMINI_MODEL}`\n"
        "• Platform: Google Gemini\n"
        "• Deploy: Railway\n"
        "• Dibuat dengan: python-telegram-bot v20",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    user_msg = update.message.text.strip()

    if not user_msg:
        return

    # Show typing indicator
    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        chat   = get_chat_session(user_id)
        response = chat.send_message(user_msg)
        reply  = response.text

        # Telegram max message length = 4096 chars
        if len(reply) > 4096:
            for i in range(0, len(reply), 4096):
                await update.message.reply_text(reply[i : i + 4096])
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logger.error("Gemini error for user %s: %s", user_id, e)
        await update.message.reply_text(
            "⚠️ Maaf, terjadi kesalahan saat memproses pesanmu.\n"
            "Coba lagi atau ketik /new untuk memulai sesi baru."
        )


async def post_init(application: Application):
    """Set bot commands in Telegram menu."""
    await application.bot.set_my_commands([
        BotCommand("start", "Mulai / Tampilkan menu"),
        BotCommand("new",   "Mulai percakapan baru"),
        BotCommand("help",  "Bantuan penggunaan"),
        BotCommand("about", "Tentang bot ini"),
    ])


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("new",   cmd_new))
    app.add_handler(CommandHandler("help",  cmd_help))
    app.add_handler(CommandHandler("about", cmd_about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started with model: %s", GEMINI_MODEL)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
