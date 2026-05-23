# This module contains the function to generate a review based on the constructed prompt and the language model.


import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from google.api_core import exceptions as google_exceptions

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.0-flash"
)


def generate_review(prompt, max_retries: int = 3, base_delay: float = 1.0) -> str:
    """Generate a review from `prompt` with simple retry/backoff on quota errors.

    Raises the original exception if retries are exhausted.
    """

    attempt = 0
    while True:
        try:
            response = model.generate_content(prompt)
            return response.text

        except google_exceptions.ResourceExhausted as e:
            attempt += 1
            if attempt > max_retries:
                print("Quota exhausted and max retries reached. Check billing/quota.")
                raise
            delay = base_delay * (2 ** (attempt - 1))
            print(f"Resource exhausted (quota). Retry {attempt}/{max_retries} in {delay}s...")
            time.sleep(delay)

        except Exception:
            # For other errors, re-raise so caller can handle/log as appropriate
            raise