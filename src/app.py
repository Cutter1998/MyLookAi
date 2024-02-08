from flask import Flask, render_template, request
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv('env_vars.env')
app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def download_png(url, filename):
    """
    Download a PNG image from the given URL and save it as a file.

    Args:
    url (str): The URL of the image.
    filename (str): The name of the file to save the image as.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded and saved as {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gen_picture_of_user', methods=['POST'])
def convert():
    user_description = {}
    user_description["gender"] = request.form['gender']
    user_description["age"] = request.form['age']
    user_description["height"] = request.form['height']
    user_description["hair_length"] = request.form['hair_length']
    user_description["hair_colour"] = request.form['hair_colour']
    user_description["eye_colour"] = request.form['eye_colour']
    user_description["build"] = request.form['build']
    user_description["race"] = request.form['race']
    user_description_image_prompt = f"Generate a photograph of a {user_description['height']}, {user_description['race']}, {user_description['build']}, {user_description['eye_colour']} eyed, {user_description['age']} year old {user_description['gender']} with {user_description['hair_colour']} hair of {user_description['hair_length']} length. They are standing, wearing black shoes with black jeans and a white t-shirt in front of a blank background with no other features or graphical elements in frame."
    image_url = generate_image(user_description_image_prompt)
    download_png(image_url, "user.png")
    return "response"

def generate_image(user_description_image_prompt):
    print(user_description_image_prompt)
    response = client.images.generate(
        model="dall-e-3", # DEFAULTS TO 2, cheaper until production
        prompt=user_description_image_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    print(image_url)
    return image_url

if __name__ == '__main__':
    app.run(debug=True)