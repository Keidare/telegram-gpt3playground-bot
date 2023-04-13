import requests
import sqlite3
import openai
# Set up the database
conn = sqlite3.connect('recipes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS recipes
             (food_name text, recipe text)''')

# Define a function to handle incoming messages
def message(input_text):
    # Get the user's message
    user_message = str(input_text).lower()
    
    if user_message.startswith('/cook'):
        words = user_message.split(' ')
        if len(words) < 2:
            # No food name provided
            return "Please provide a food name."
        
        food_name = ' '.join(words[1:])

        openai.api_key = "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"
        prompt = f"Generate a recipe for {food_name}."
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user",
                       "content": prompt}]
        )
        recipe = completions.choices[0].message.content

        # Store the recipe in the database


        # Send the recipe back to the user
        return recipe
    
    elif user_message.startswith('/listfood'):
        # Retrieve all the foods cooked by the user from the database
        c.execute("SELECT food_name FROM recipes")
        foods = c.fetchall()
        
        # Send the list of foods back to the user
        foods_str = '\n'.join([f[0] for f in foods])
        return foods_str
    
    elif user_message.startswith('/viewrecipe'):
        # Parse the food name from the user's message
        food_name = user_message.split(' ')[1]
        
        # Retrieve the recipe for the food from the database
        c.execute("SELECT recipe FROM recipes WHERE food_name=?", (food_name))
        recipe = c.fetchone()
        
        # Send the recipe back to the user
        if recipe is not None:
            return recipe[0]
        else:
           return f"No recipe found for {food_name}."

