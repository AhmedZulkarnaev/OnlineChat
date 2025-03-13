from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import random
import os

templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/join_chat", response_class=HTMLResponse)
async def join_chat(
    request: Request, username: str = Form(...), room_id: int = Form(...)
):
    user_id = random.randint(100, 10000)
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "room_id": room_id,
                                       "username": username,
                                       "user_id": user_id}
                                      )
