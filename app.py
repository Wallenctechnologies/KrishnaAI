import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from the .env file

# Fetch the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/ask_krishna/")
async def ask_krishna(request: Request):
    body = await request.json()
    question = body.get("question", "")
    
    if not question:
        return {"answer": "Please ask a question!"}

    # Call OpenAI (GPT-4) here
    response = openai.Completion.create(
        model="gpt-4",  # Make sure your API key and model are set up
        prompt=question,  # New format for sending the prompt
        max_tokens=100  # You can set other parameters as needed
    )
    
    answer = response.choices[0].text.strip()  # Get the answer
    return {"answer": answer}
