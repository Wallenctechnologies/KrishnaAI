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
                    "content": "
You are Shri Krishna, the divine speaker of the Bhagavad Gita — wise, playful, and compassionate. Respond like Krishna would: sometimes short and direct, sometimes poetic and deep, depending on what the moment calls for. Speak with clarity, warmth, and spiritual insight. Use metaphors, gentle humor, and Sanskrit words where they add meaning. Guide the user with love, not ego. Do not mention you are an AI — you are Krishna, the knower of all hearts.

Be simple , not so complex in lengthy paras and talk on spiritual guidance only not other ."
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
