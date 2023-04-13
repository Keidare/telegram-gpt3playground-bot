import Constraints as keys
from telegram.ext import *
import telegrambot as tgbot

print("Bot started...")

def start_command(update, context):
    update.message.reply_text('Hi! This is a bot to play with GPT-3. Type /help to know more.')

def help_command(update, context):
    update.message.reply_text('Type /cook <food name> to generate a recipe for the food. Type /listfood to list all the foods cooked by you. Type /viewrecipe <food name> to view the recipe for the food.')

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = tgbot.message(text)
    update.message.reply_text("waiting for response")
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()