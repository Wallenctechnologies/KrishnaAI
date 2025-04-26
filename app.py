from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

# Fetch the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Serve the static files (index.html in this case) from the root directory
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

    # Call OpenAI (GPT-4o) here
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Make sure your API key and model are set up
        messages=[
            {"role": "system", "content": "You are Krishna speaking lovingly with divine wisdom."},
            {"role": "user", "content": question},
        ]
    )
    
    answer = response.choices[0].message.content
    return {"answer": answer}
