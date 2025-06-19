import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def match_headers(col1, col2):
    # Your LLM prompt and response processing
    ...
