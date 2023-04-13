import requests
import sqlite3
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
        # Parse the food name from the user's message
        food_name = user_message.split(' ')[1]

        # Use the GPT-3 Playground API to generate a recipe for the food
        response = requests.post('https://api.openai.com/v1/playground/translate',
                                headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer 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'},
                                json={'text': f'Generate a recipe for {food_name}.',
                                    'model': 'text-davinci-002'})
        if response.status_code != 200:
            print(f"API call failed with status code {response.status_code}: {response.content}")
            return "Sorry, I could not generate a recipe at this time. Please try again later."

        try:
            recipe = response.json()['data']['translation']
        except KeyError:
            print(f"Unexpected response format: {response.content}")
            return "Sorry, I could not understand the API response. Please try again later."

        # Store the recipe in the database
        c.execute("INSERT INTO recipes VALUES (?, ?)", (food_name, recipe))
        conn.commit()

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

