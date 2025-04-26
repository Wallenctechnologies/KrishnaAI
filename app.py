from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file (if running locally)
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Set up OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Jai Shri Krishna! Your AI Assistant is running!"}

@app.post("/ask_krishna/")
async def ask_krishna(question: str):
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # You can switch to `gpt-4` for more advanced responses
            prompt=f"Answer the following question in the style of Lord Krishna: {question}",
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
