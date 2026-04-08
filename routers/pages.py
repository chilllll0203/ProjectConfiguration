from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from deps import get_session
from models import AchievementModel, EventModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()

# Шаблонизатор для загрузки html-страниц
templates = Jinja2Templates(directory="templates")

# Личный кабинет студента
@router.get("/person_account_student")
def person_account_student(request: Request):
    username = request.session["username"]
    return templates.TemplateResponse("personal_account_student.html", {"request": request, "username": username})
@router.post("/person_account_student")
def person_account_student(request: Request, option: str = Form(...)):
    user_id = request.session["user_id"]
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_student.html",{"request": request, "username": username})
    elif option == "view_your_achievements":
        return RedirectResponse("/view_your_achievements", status_code=303)
    elif option == "add_achievements":
        return templates.TemplateResponse("add_achievements.html", {"request": request})
    elif option == "settings":
        return templates.TemplateResponse("settingsstudent.html", {"request": request, "username": username, "email": email})

# Личный кабинет преподавателя
@router.get("/person_account_teacher")
def person_account_teacher(request: Request):
    username = request.session["username"]
    return templates.TemplateResponse("personal_account_teacher.html", {"request": request, "username": username})
@router.post("/person_account_teacher")
def person_account_teacher(request: Request,option: str = Form(...)):
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_teacher.html",{"request": request, "username": username})
    elif option == "view_all_events":
        return RedirectResponse("/events", status_code=303)
    elif option == "add_event":
        return templates.TemplateResponse("add_event.html",{"request": request})
    elif option == "settings":
        return templates.TemplateResponse("settingsteacher.html",{"request": request, "username": username, "email": email})

# Личный кабинет администратора
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
        return templates.TemplateResponse("settingsadmin.html", {"request": request,"username": username,"email": email})

# Настройки личного кабинета для администратора
@router.get("/setingsadmin")
def setings_admin(request: Request, option: str = Form(...)):
    username = request.session["username"]
    email = request.session["email"]
    return templates.TemplateResponse("settingsadmin.html", {"request": request, "username": username, "email": email})
@router.post("/setingsadmin")
def setings_admin(request: Request, option: str = Form(None),changepassword: str = Form(None),exitaccount:str = Form(None)):
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_administrator.html",{"request": request, "username": username})
    elif option == "table_users":
        return RedirectResponse("/users", status_code=303)
    elif option == "table_events":
        return RedirectResponse("/events", status_code=303)
    elif option == "table_achievements":
        return RedirectResponse("/achievements", status_code=303)
    elif option == "settings":
        return templates.TemplateResponse("settingsadmin.html", {"request": request, "username": username, "email": email})
    if changepassword == "change":
        return "Пока эта функция не реализована!"
    if exitaccount == "exit":
        request.session.clear()
        return RedirectResponse("/", status_code=303)

# Добавление достижения студента(может добавлять только студент)
@router.get("/add_achievements")
def add_achievements(request: Request, option: str = Form(None)):
    return templates.TemplateResponse("add_achievements.html", {"request": request})
@router.post("/add_achievements")
async def add_achievements(request: Request, option: str = Form(None),nameEvent:str = Form(...),category:str = Form(...),result:str = Form(...),document_url:str = Form(...),addachievement:str = Form(None),session: AsyncSession = Depends(get_session)):
    user_id = request.session["user_id"]
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_student.html",{"request": request, "username": username})
    elif option == "view_your_achievements":
        return RedirectResponse("/view_your_achievements", status_code=303)
    elif option == "add_achievements":
        return templates.TemplateResponse("add_achievements.html", {"request": request})
    elif option == "settings":
        return templates.TemplateResponse("settingsstudent.html", {"request": request, "username": username, "email": email})
    if addachievement == "addachievement":
        result = await session.execute(select(EventModel).where(EventModel.title == nameEvent))
        event = result.scalars().first()
        achievement = AchievementModel(
            student_id = user_id,
            event_id = event.id,
            category = category,
            result = result,
            document_url = document_url,
            create_date = datetime.now()
        )
        session.add(achievement)
        await session.commit()
        return RedirectResponse("/view_your_achievements", status_code=303)


# Добавление мероприятия (может добавлять только преподаватель)
@router.get("/add_event")
def add_achievements(request: Request, option: str = Form(None)):
    return templates.TemplateResponse("add_achievements.html", {"request": request})
@router.post("/add_event")
async def add_achievements(request: Request, option: str = Form(None),title:str = Form(...),description:str = Form(...),event_date:str = Form(...),type:str = Form(...),addevent:str = Form(None),session: AsyncSession = Depends(get_session)):
    user_id = request.session["user_id"]
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_teacher.html", {"request": request, "username": username})
    elif option == "view_all_events":
        return RedirectResponse("/events", status_code=303)
    elif option == "add_event":
        return templates.TemplateResponse("add_event.html", {"request": request})
    elif option == "settings":
        return templates.TemplateResponse("settingsteacher.html",{"request": request, "username": username, "email": email})
    if addevent == "addevent":
        event = EventModel(
            title = title,
            description = description,
            event_date = event_date,
            type = type,
            created_by = user_id,
            created_at = datetime.now()
        )
        await session.commit()
        return RedirectResponse("/events", status_code=303)


# Настройки личного кабинета для студента
@router.get("/setingsstudent")
def setings_student(request: Request, option: str = Form(...)):
    username = request.session["username"]
    email = request.session["email"]
    return templates.TemplateResponse("settingsstudent.html", {"request": request, "username": username, "email": email})
@router.post("/setingsstudent")
def setings_student(request: Request, option: str = Form(None),changepassword: str = Form(None),exitaccount:str = Form(None)):
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_student.html", {"request": request, "username": username})
    elif option == "view_your_achievements":
        return RedirectResponse("/view_your_achievements", status_code=303)
    elif option == "add_achievements":
        return templates.TemplateResponse("add_achievements.html", {"request": request})
    elif option == "settings":
        return templates.TemplateResponse("settingsstudent.html",{"request": request, "username": username, "email": email})
    if changepassword == "change":
        return "Пока эта функция не реализована!"
    if exitaccount == "exit":
        request.session.clear()
        return RedirectResponse("/", status_code=303)

# Настройки личного кабинета для преподавателя
@router.get("/setingsteacher")
def setings_teacher(request: Request, option: str = Form(...)):
    username = request.session["username"]
    email = request.session["email"]
    return templates.TemplateResponse("settingsstudent.html", {"request": request, "username": username, "email": email})
@router.post("/setingsstudent")
def setings_teacher(request: Request, option: str = Form(None),changepassword: str = Form(None),exitaccount:str = Form(None)):
    username = request.session["username"]
    email = request.session["email"]
    if option == "home":
        return templates.TemplateResponse("personal_account_teacher.html", {"request": request, "username": username})
    elif option == "view_all_events":
        return RedirectResponse("/events", status_code=303)
    elif option == "add_event":
        return templates.TemplateResponse("add_event.html", {"request": request})
    elif option == "settings":
        return templates.TemplateResponse("settingsteacher.html",{"request": request, "username": username, "email": email})
    if changepassword == "change":
        return "Пока эта функция не реализована!"
    if exitaccount == "exit":
        request.session.clear()
        return RedirectResponse("/", status_code=303)
