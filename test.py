import openai
import pandas as pd

# Load your CSV data into a DataFrame
food_data = pd.read_csv('food.csv')

# Set your OpenAI API key
openai.api_key = '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'

def get_calories(food_item):
    # Check if the food item is in the loaded CSV data
    if food_item.lower() in food_data['Food'].str.lower().values:
        # Retrieve the calories for the given food item
        calories = food_data.loc[food_data['Food'].str.lower() == food_item.lower(), 'Calories'].values[0]
        return calories
    else:
        return None

def ask_openai(question):
    # Generate a prompt for OpenAI based on the question
    prompt = f"Tell me the calories of {question}."

    # Use OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}        ]
    )

    chatgpt_response = response.choices[0].message['content']
    return chatgpt_response



# Example usage
food_item = input("you:")
food_items = [food.strip() for food in food_item.split(',')]

total_calories = 0
# calories = get_calories(food_item)

for food_item in food_items:
    calories = get_calories(food_item)
    if calories is not None:
        total_calories += calories
        print(f"{food_items} has {total_calories} calories.")
    else:
        print(f"Sorry, {food_item} not found in the database.")


if calories is not None:
    question = f"How many calories does {food_item} have?"
    answer = ask_openai(question)

    print(f"OpenAI says: {answer}")
else:
    print(f"Sorry, {food_item} not found in the database.")
