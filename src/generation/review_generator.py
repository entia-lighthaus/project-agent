# This module contains the function to generate a review based on the constructed prompt and the language model.


import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.0-flash"
)


def generate_review(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text