from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers import gemini_analysis
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

load_dotenv()  # .env faylını oxuyur

app = FastAPI()
app.include_router(gemini_analysis.router)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
