from fastapi import APIRouter, Request, Form, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from deps import get_session
from models import AchievementModel, EventModel

router = APIRouter()

# Шаблонизатор для загрузки html-страниц
templates = Jinja2Templates(directory="templates")


@router.get("/person_account_student")
def person_account(request: Request):
    username = request.session["username"]
    return f"Добро пожаловать студент {username} !"

@router.get("/person_account_teacher")
def person_account(request: Request):
    username = request.session["username"]
    return f"Добро пожаловать преподаватель {username} !"

@router.get("/person_account_administrator")
def person_account(request: Request):
    username = request.session["username"]
    return f"Добро пожаловать администратор {username} !"