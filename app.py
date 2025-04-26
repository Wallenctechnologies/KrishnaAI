from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Jai Shri Krishna! Your AI Assistant is running!"}
