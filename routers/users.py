from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import bcrypt
from starlette.middleware.sessions import SessionMiddleware

from models import UserModel
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