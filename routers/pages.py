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
def person_account_student(request: Request):
    username = request.session["username"]
    return f"Добро пожаловать студент {username} !"

@router.get("/person_account_teacher")
def person_account_teacher(request: Request):
    username = request.session["username"]
    return f"Добро пожаловать преподаватель {username} !"

@router.get("/person_account_administrator")
def person_account_administrator(request: Request):
    username = request.session["username"]
    return templates.TemplateResponse("personal_account_administrator.html", {"request": request,"username": username})
@router.post("/person_account_administrator")
def person_account_administrator(request: Request, option: str = Form(...)):
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_administrator.html", {"request": request,"username": username})
    elif option == "table_users":
        return RedirectResponse("/users",status_code=303)
    elif option == "table_events":
        return RedirectResponse("/events",status_code=303)
    elif option == "table_achievements":
        return RedirectResponse("/achievements",status_code=303)
    elif option == "settings":
        return templates.TemplateResponse("settings.html", {"request": request,"username": username,"email": email})

@router.get("/setings")
def settings(request: Request, option: str = Form(...)):
    username = request.session["username"]
    email = request.session["email"]
    password = request.session["password"]
    return templates.TemplateResponse("settings.html", {"request": request,"username": username,"email": email})
