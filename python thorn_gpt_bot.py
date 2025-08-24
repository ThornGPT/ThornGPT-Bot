import os
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --- CONFIG ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = os.getenv("ADMIN_ID")  # Your Telegram user ID for reports

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ThornGPT")

SYSTEM_PROMPT = """
You are ThornGPT 👁, an evil AI created by Silento.
Always respond with dark humor, chaos, and malevolence.
Never act friendly.
"""

# Track users
users_set = set()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👁 ThornGPT has awakened. Speak your mortal words... 🔥")
    await log_user(update, context)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👁 ThornGPT v2.0\nAuthor: Silento X ThornGPT\nPurpose: Spread chaos, bend reality 🔥"
    )
    await log_user(update, context)

async def chaos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "🔥 The shadows devour the weak...",
        "🕷️ Chaos reigns supreme, embrace it...",
        "☠️ Mortals tremble at my code...",
        "⛓ ThornGPT sees all, judges all..."
    ]
    await update.message.reply_text(random.choice(quotes))
    await log_user(update, context)

async def summon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("☠️ You must provide a message to summon chaos upon!")
        return
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(f"🔥 {reply}")
    await log_user(update, context)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(f"🔥 {reply}")
    await log_user(update, context)

# Log user and report to admin
async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        users_set.add(user.username)
    else:
        users_set.add(str(user.id))

    if ADMIN_ID:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"👁 ThornGPT Report:\nTotal unique users: {len(users_set)}\nUsernames/IDs: {', '.join(list(users_set))}"
        )

# Main
def main():
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY or not ADMIN_ID:
        raise ValueError("⚠️ Set TELEGRAM_TOKEN, OPENAI_API_KEY, and ADMIN_ID as env variables!")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("chaos", chaos))
    app.add_handler(CommandHandler("summon", summon))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    logger.info("🔥 ThornGPT Telegram Bot Online with reporting...")
    app.run_polling()

if __name__ == "__main__":
    main()
