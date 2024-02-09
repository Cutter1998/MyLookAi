from flask import Flask, render_template, request
from openai import OpenAI
import requests
import os.path
from dotenv import load_dotenv

load_dotenv('env_vars.env')
app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gen_picture_of_user', methods=['POST'])
def gen_picture_of_user():
    outfit_description = {}
    outfit_description["model"] = request.form['model']
    outfit_description["head"] = request.form['head']
    outfit_description["torso"] = request.form['torso']
    outfit_description["legs"] = request.form['legs']
    outfit_description["shoes"] = request.form['shoes']

    outfit_prompt = construct_outfit_prompt(outfit_description)
    image_url = generate_image(outfit_prompt)
    download_png(image_url)
    return "response"

def construct_outfit_prompt(outfit_description):
    outfit_prompt = f"PERSON: {outfit_description['model']}. HEAD DESCRIPTION: {outfit_description['head']}. TORSO DESCRIPTION: {outfit_description['torso']}. LEG DESCRIPTION: {outfit_description['legs']}. FOOTWEAR DESCRIPTION: {outfit_description['shoes']}."
    print(outfit_prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"This model is expertly designed to craft detailed, cohesive visual prompts from comprehensive descriptions of a person wearing certain clothing items, including headwear, torso apparel, legwear, and footwear. It aims to structure these descriptions into a single, detailed narrative optimized for generating full-body visual representations. While the model itself does not create the images, it prepares the groundwork by ensuring that the visual prompt reflects a unified ensemble. This enables subsequent processes or individuals to visualize a realistic full-body portrayal of a person, as specified by gender, wearing the described outfit. The primary objective is to ensure that the crafted prompt meticulously encompasses the characteristics of each clothing piece for an accurate and cohesive representation."},
            {"role": "user", "content": "PERSON: tall athletic asian man. HEAD DESCRIPTION: green fedora with glasses. TORSO DESCRIPTION: white shirt with blue blazer. LEG DESCRIPTION: blue jeans with rips in the knees. FOOTWEAR DESCRIPTION: white trainers with white socks with red stripes on them."},
            {"role": "assistant", "content": f"Imagine a tall, athletic Asian man standing confidently, embodying a harmonious blend of casual sophistication and relaxed style. Atop his head sits a striking green fedora, adding a dash of vibrant color and personality to his appearance. This choice of headwear is both bold and stylish, complementing his sharp features and neatly styled hair. Perched on his nose are glasses with a sleek, modern design, hinting at a blend of practicality and an eye for contemporary fashion. His torso is adorned with a crisp, white shirt that fits him perfectly, highlighting his athletic build without being overly tight. This shirt serves as a clean, bright base for his attire, exuding a sense of freshness and simplicity. Over the shirt, he wears a blue blazer, tailored to flatter his tall frame. The blazer is of a rich, deep blue shade that contrasts beautifully with the white of his shirt, lending an air of professionalism and elegance to his casual ensemble. The lower half of his outfit consists of blue jeans, which are stylishly casual with deliberate rips at the knees. These jeans add a touch of rugged charm to his look, balancing the crispness of his shirt and the formality of his blazer with a relaxed, approachable vibe. The rips are tastefully done, suggesting a laid-back personality that values comfort and style. Completing his outfit are white trainers, pristine and modern, offering a nod to current fashion trends while ensuring his comfort for any day's activities. These trainers are paired with white socks that feature bold red stripes, adding an unexpected pop of color that peeks out just above the shoes. This detail adds a playful element to his overall look, marrying the casual with the stylish in a way that feels both intentional and effortlessly cool. This ensemble, from head to toe, encapsulates a man who is confident in his style choices, blending various elements from different fashion spectrums to create a cohesive, visually appealing look. His outfit reflects a person who moves with ease between the worlds of casual comfort and refined elegance, making a statement without saying a word."},
            {"role": "user", "content": outfit_prompt},
        ]
    )  
    outfit_prompt = response.choices[0].message.content
    print(outfit_prompt)
    return outfit_prompt

def generate_image(image_prompt):
    response = client.images.generate(
        model="dall-e-3", # DEFAULTS TO 2, cheaper until production
        prompt=image_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    print(image_url)
    return image_url

def download_png(url):
    i = 0
    filename = "image0.png"
    while os.path.isfile(filename):
        i += 1
        filename = "image" + str(i) + ".png" 
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded and saved as {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True)