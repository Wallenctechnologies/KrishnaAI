from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve the homepage
@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content

# Pydantic model for the incoming question
class Question(BaseModel):
    question: str

# Handle the question submission
@app.post("/ask_krishna/")
async def ask_krishna(question: Question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # use gpt-4o
            messages=[
                {
                    "role": "system",
                    "content": "You are Krishna, a compassionate, wise, and playful teacher who answers with love, deep insight, and joy."
                },
                {
                    "role": "user",
                    "content": question.question
                }
            ],
            temperature=0.7,
            max_tokens=500,
        )
        krishna_reply = response["choices"][0]["message"]["content"].strip()
        return {"answer": krishna_reply}
    except openai.error.AuthenticationError:
        return {"error": "Authentication failed. Please check your API key."}
    except openai.error.OpenAIError as e:
        return {"error": f"OpenAI API error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
