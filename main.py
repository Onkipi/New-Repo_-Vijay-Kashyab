import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq

TELEGRAM_TOKEN = os.environ.get("8412781561:AAHsigyvWrSoJRZFi8T8T_zBf4LcEy3Kq2Q")
GROQ_API_KEY = os.environ.get("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")

client = Groq(api_key=GROQ_API_KEY)

async def handle_message(update, context):
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful personal AI assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running!")
    await app.run_polling()

asyncio.run(main())
