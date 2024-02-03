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
            {"role": "user", "content": prompt}
        ]
    )

    chatgpt_response = response.choices[0].message['content']
    return chatgpt_response

def calculate_total_calories(food_items):
    total_calories = 0

    for food_item in food_items:
        calories = get_calories(food_item)
        if calories is not None:
            total_calories += calories
            print(f"{food_item} has {calories} calories.")
        else:
            print(f"Sorry, {food_item} not found in the database.")

    print(f"\nTotal calories for all foods: {total_calories}")

    # Optionally, you can ask OpenAI for a summary or additional information
    question = "Tell me about the nutritional content of the foods."
    answer = ask_openai(question)
    print(f"\nOpenAI says: {answer}")

if __name__ == "__main__":
    food_input = input("you:")
    food_items_list = [food.strip() for food in food_input.split(',')]
    calculate_total_calories(food_items_list)
