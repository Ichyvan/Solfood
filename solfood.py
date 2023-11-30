import openai
import json
from IPython.display import display, Image

# # OpenAI API 키
with open('C:\Users\이창현\Desktop\Amplify\app\secrets.json') as f:
    secrets = json.load(f)
    SECRET_KEY = secrets['Secret_key']

openai.api_key = SECRET_KEY

def generate_food_name_and_recipe(ingredients):
    # 재료를 이용해 음식 이름과 레시피를 생성하는 prompt를 구성합니다.
    prompt = f"Generate the name and recipe of a simple dish using the following ingredients: {', '.join(ingredients)}."

    # OpenAI API를 호출하여 음식 이름과 레시피 생성
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None
    )

    # 생성된 텍스트에서 음식 이름과 레시피를 추출
    choices = response['choices']
    if choices:
        generated_text = choices[0]['text']
        # 음식 이름 추출
        food_name_start = generated_text.find("Food Name:") + len("Food Name:")
        food_name_end = generated_text.find("Recipe:")
        food_name = generated_text[food_name_start:food_name_end].strip()
        # 레시피 추출
        recipe_start = generated_text.find("Recipe:") + len("Recipe:")
        recipe = generated_text[recipe_start:].strip()

        return food_name, recipe
    else:
        return None, None

def generate_food_image(food_name):
    # 음식 이름을 이용해 이미지를 생성하는 prompt를 구성합니다.
    prompt = f"Generate an image of a very delicious looking dish named {food_name}."

    # OpenAI API를 호출하여 이미지 생성
    response = openai.Image.create(
        prompt = prompt,
        n=1,
        size = '1024x1024'
    )

    # 생성된 이미지의 URL을 추출
    choices = response['data']
    if choices:
        image_url = choices[0]['url']
        return image_url
    else:
        return None

# 사용자로부터 재료를 입력 받습니다.
user_ingredients = input("Enter the ingredients you have (comma-separated): ").split(',')

# OpenAI API를 사용하여 음식 이름과 레시피 생성
food_name, food_recipe = generate_food_name_and_recipe(user_ingredients)

# 음식 이미지 생성
food_image_url = generate_food_image(food_name)

# 결과를 출력
if food_name and food_recipe and food_image_url:
    print(f"Food Name: {food_name}")
    print(f"Generated Food Image:")
    print(food_image_url)
    display(Image(url=food_image_url))
else:
    print("Failed to generate food name, recipe, or image.")