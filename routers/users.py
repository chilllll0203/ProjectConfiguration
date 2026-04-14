from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import bcrypt
from starlette.middleware.sessions import SessionMiddleware

from models import UserModel,AchievementModel,EventModel
from deps import get_session

router = APIRouter()

# Шаблонизатор для загрузки html-страниц
templates = Jinja2Templates(directory="templates")

@router.get("/users",summary="Получение пользователей")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UserModel))
    users = result.scalars().all()  # scalars() превращает Result в объекты модели
    with open("log.txt", "a", encoding="utf-8") as file:
        file.writelines("Администратор запросил таблицу с пользователями " + datetime.now().isoformat() + "\n")
    # Конвертируем в словари для JSON
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.hashed_password,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]
@router.get("/events",summary="Получение мероприятий")
async def get_events(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(EventModel))
    events = result.scalars().all()  # scalars() превращает Result в объекты модели
    with open("log.txt", "a", encoding="utf-8") as file:
        file.writelines("Администратор запросил таблицу с мероприятиями " + datetime.now().isoformat() + "\n")
    # Конвертируем в словари для JSON
    return [
        {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_date": event.event_date.isoformat(),
            "type": event.type,
            "created_by": event.created_by,
            "created_at": event.created_at.isoformat(),
        }
        for event in events
    ]
@router.get("/achievements",summary="Получение достижений")
async def get_achievements(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(AchievementModel))
    achievements = result.scalars().all()  # scalars() превращает Result в объекты модели
    with open("log.txt", "a", encoding="utf-8") as file:
        file.writelines("Администратор запросил таблицу с достижениями " + datetime.now().isoformat() + "\n")
    # Конвертируем в словари для JSON
    return [
        {
            "id": achievement.id,
            "student_id": achievement.student_id,
            "event_id": achievement.event_id,
            "category": achievement.category,
            "result": achievement.result,
            "document_url": achievement.document_url,
            "created_at": achievement.created_at.isoformat(),
        }
        for achievement in achievements
    ]

@router.get("/view_your_achievements",summary="Получение достижений определенного пользователя")
async def view_your_achievements(request: Request,session: AsyncSession = Depends(get_session)):
    username = request.session["username"]
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    result = await session.execute(select(AchievementModel).where(AchievementModel.student_id == user.id))
    achievements = result.scalars().all()
    return [
        {
            "id": achievement.id,
            "student_id": achievement.student_id,
            "event_id": achievement.event_id,
            "category": achievement.category,
            "result": achievement.result,
            "document_url": achievement.document_url,
            "created_at": achievement.created_at.isoformat(),
        }
        for achievement in achievements
    ]