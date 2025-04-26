import openai
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

load_dotenv()  # This loads your .env file

# Fetch the OpenAI API Key from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

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
