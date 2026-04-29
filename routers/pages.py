from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException, Body, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from deps import get_session
from models import AchievementModel, EventModel, TelegramAuthenticationModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jwt import PyJWKClient, PyJWKClientError
import jwt
import time
import logging
from models import UserModel
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)

# Профиль пользователей(выбирается в зависимости от роли)
@router.get("/profile")
def profile(request: Request):
    role = request.session["role"]
    if (role == "student"):
        return templates.TemplateResponse(request,"personal_account_student.html")
    elif (role == "teacher"):
        return templates.TemplateResponse(request,"personal_account_teacher.html")
    elif (role == "administrator"):
        return templates.TemplateResponse(request,"personal_account_administrator.html")
    else:
        return "Произошла ошибка попробуйте снова!"

# Настройки пользователей(выбирается в зависимости от роли)
@router.get("/settings")
def settings(request: Request):
    role = request.session["role"]
    if (role == "student"):
        return templates.TemplateResponse(request, "settingsstudent.html",{"username":request.session["username"],"email":request.session["email"]})
    elif (role == "teacher"):
        return templates.TemplateResponse(request, "settingsteacher.html",{"username":request.session["username"],"email":request.session["email"]})
    elif (role == "administrator"):
        return templates.TemplateResponse(request, "settingsadmin.html", {"username":request.session["username"],"email":request.session["email"]})
    else:
        return "Произошла ошибка попробуйте снова!"
    
# Функция на проверку роли студента, если не студент выкидывает  ошибку, иначе дает доступ на страницу с достижениями определенного студента.
@router.get("/achievements")
def achievements(request: Request):
    role = request.session["role"]
    if (role != "student"):
        raise  HTTPException(status_code=403,detail="Access forbidden")
    return templates.TemplateResponse(request, "achievements.html")

# Получени токена пользователя с телеграмма
@router.post("/tg_auth")
async def tg_auth(request: Request,
             id_token: str = Body(),
             session: AsyncSession = Depends(get_session)):
    try:
        CLIENT_ID = "8758842032"
        jwks = PyJWKClient("https://oauth.telegram.org/.well-known/jwks.json")
        key = jwks.get_signing_key_from_jwt(id_token)
        payload = jwt.decode(id_token, key.key, algorithms = ["RS256"])
        
        if payload.get("iss") != "https://oauth.telegram.org":
            raise ValueError(f"Неверный issuer: {payload['iss']}")
        
        aud = payload.get("aud")
        if isinstance(aud, list):
            if CLIENT_ID not in aud:
                raise ValueError("Неверная аудитория")
        elif aud != CLIENT_ID:
            raise ValueError(f"Неверная аудитория: {aud}")
        
        if time.time()>payload.get("exp",0):
            raise ValueError("Токен истек")
        
        if payload.get("iat",0) > time.time+60:
            raise ValueError("Токен выпущен в будущем - возможна подделка")
        
        userID = request.session["user_id"]
        telegramUser = TelegramAuthenticationModel(
            userID = userID,
            telegramId = payload.get("id")
        )
        session.add(telegramUser)
        await session.commit()
    except PyJWKClientError as e:
        logging.error(f"Ошибка JWKS: {e}")
        raise HTTPException(status_code=400,detail="Invalid Token Format")
    except jwt.InvalidTokenError as e:
        logging.error(f"Невалидный токен: {e}")
        raise HTTPException(status_code=401,detail="Invalid Token")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    logging.info(f"Была создана связка telegram: {telegramUser.telegramId}, user: {telegramUser.userId}"+"\n")
    
# Страница добавления достижения
@router.get("/add_achievements")
def add_achievements_get(request: Request):
    return templates.TemplateResponse(request, "add_achievements.html")
@router.post("/add_achievements")
async def add_achievements_post(
        request: Request,
        nameEvent: str = Form(None),
        category: str = Form(None),
        result_achievement: str = Form(None),
        document_url: str = Form(None),
        addachievement: str = Form(None),
        session: AsyncSession = Depends(get_session)
):
    if addachievement == "addachievement":
        result = await session.execute(select(EventModel).where(EventModel.title == nameEvent))
        event = result.scalars().first()
        if event:
            achievement = AchievementModel(
                student_id=request.session["user_id"],
                event_id=event.id,
                category=category,
                result=result_achievement,
                document_url=document_url,
                created_at=datetime.now()
            )
            session.add(achievement)
            await session.commit()
        return RedirectResponse("/achievements", status_code=303)

# Страница добавления мероприятия
@router.get("/add_event")
def add_event_get(request: Request):
    return templates.TemplateResponse(request, "add_event.html")
@router.post("/add_event")
async def add_event_post(
        request: Request,
        title: str = Form(...),
        description: str = Form(...),
        event_date: str = Form(...),
        type: str = Form(...),
        addevent: str = Form(None),
        session: AsyncSession = Depends(get_session)
):
    if addevent == "addevent":
        event = EventModel(
            title=title,
            description=description,
            event_date=datetime.strptime(event_date, '%Y-%m-%d').date(),
            type=type,
            created_by=request.session["user_id"],
            created_at=datetime.now()
        )
        session.add(event)
        await session.commit()
        return RedirectResponse("/events", status_code=303)

# Страница смены пароля 
@router.get("/change_password")
def change_password(request:Request):
    return templates.TemplateResponse(request,"change_password.html")
@router.post("/change_password")
async def change_password(request:Request,current_password: str = Form(...),new_password: str = Form(...),button_change: str = Form(None),session: AsyncSession = Depends(get_session)):
    user_id = request.session["user_id"]
    if button_change:
        result = await session.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalars().first()
        if bcrypt.checkpw(current_password.encode("utf-8"), user.hashed_password):
            user.hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
            await session.commit()
            await session.refresh(user)
    return RedirectResponse("/settings",status_code=303)
