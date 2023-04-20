from telegram.ext import *
import sqlite3
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
tg_api_key = os.getenv("TG_API_KEY")

# Set up the database
print("Bot started...")


def start_command(update, context):
    update.message.reply_text('Hi! This is a bot to play with GPT-3. Type /help to know more.')

def help_command(update, context):
    update.message.reply_text('Type /cook <food name> to generate a recipe for the food. Type /listfood to list all the foods cooked by you. Type /viewrecipe <food name> to view the recipe for the food.')

def handle_message(update, context):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                (id INTEGER PRIMARY KEY, food_name text, recipe text)''')
    user_message =  str(update.message.text).lower()
    
    if user_message.startswith('/cook'):
        words = user_message.split(' ')
        if len(words) < 2:
            # No food name provided
            return "Please provide a food name."
        
        food_name = ' '.join(words[1:])

        openai.api_key = openai_api_key
        prompt = f"Generate a recipe for {food_name}."
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user",
                       "content": prompt}]
        )
        recipe = completions.choices[0].message.content

        # Store the recipe in the database
        c.execute("INSERT INTO recipes (food_name, recipe) VALUES (?, ?)", (food_name, recipe))
        conn.commit()

        # Send the recipe back to the user
        response = recipe
    
    elif user_message.startswith('/listfood'):
        # Retrieve all the foods cooked by the user from the database
        c.execute("SELECT food_name FROM recipes")
        foods = c.fetchall()
        
        # Send the list of foods back to the user
        foods_str = '\n'.join([f[0] for f in foods])
        response = foods_str
    
    elif user_message.startswith('/viewrecipe'):
        # Parse the food name from the user's message
        words = user_message.split(' ')
        if len(words) < 2:
            # No food name provided
            return "Please provide a food name."
        
        food_name = ' '.join(words[1:])
        
        # Retrieve the recipe for the food from the database
        c.execute("SELECT recipe FROM recipes WHERE food_name=?", (food_name,))
        recipe = c.fetchone()
        
        # Send the recipe back to the user
        if recipe is not None:
            response = recipe[0]
        else:
           response = f"No recipe found for {food_name}."
           
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(tg_api_key, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()