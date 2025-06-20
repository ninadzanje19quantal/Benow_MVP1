import google.genai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class matched_columns(BaseModel):
    file1_column: str
    file2_column: str

def match_headers(col1, col2):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Take the following list of column names {col1} and match it with the {col2}. "
                  "When the matching is to be done identify the names column names with similar meanings. "
                  "Even they should be counted. Also consider all the columns from both the files."
                  "When giving the output only give me the column names do not give me anything else in response string. "
                  "For the columns that do not have any match keep it as __IGNORE__ (a string with blank string)",
        config={"response_mime_type": "application/json",
                "response_schema": list[matched_columns],},
    )
    return response.parsed