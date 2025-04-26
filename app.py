from dotenv import load_dotenv
import os

load_dotenv()  # This loads your .env file, where OPENAI_API_KEY is stored

# Fetch the OpenAI API Key from the environment variables
openai.api_key = os.getenv("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")  # Use this API key for making requests

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask_krishna/")
async def ask_krishna(request: Request):
    body = await request.json()
    question = body.get("question", "")
    
    if not question:
        return {"answer": "Please ask a question!"}

    # Call OpenAI (GPT-4o) here
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # make sure your API key and model are set up
        messages=[
            {"role": "system", "content": "You are Krishna speaking lovingly with divine wisdom."},
            {"role": "user", "content": question},
        ]
    )
    
    answer = response.choices[0].message.content
    return {"answer": answer}
