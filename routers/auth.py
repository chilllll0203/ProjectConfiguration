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

@router.get("/")  # или ваш путь, например "/"
def login_user(request: Request):
    return templates.TemplateResponse(request, "extrance.html")
@router.post("/", summary="Вход в кабинет и проверка на совпадение пользователя")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["email"] = user.email
    request.session["role"] = user.role
    if(user.username == username and bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8"))):
        return RedirectResponse("/profile",status_code=303)


@router.get("/register", summary="Форма регистрации")
def get_form(request: Request):
    return templates.TemplateResponse(request, "reg.html")

@router.post("/register", summary="Добавление пользователя")
async def add_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    roles: str = Form(...),
    session: AsyncSession = Depends(get_session)  # Используем dependency injection
):
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = UserModel(
        username=username,
        email=email,
        hashed_password=password_hash.decode("utf-8"),
        role=roles,
        created_at=datetime.utcnow()  # UTC время
    )
    session.add(user)
    await session.commit()
    with open("log.txt", "a", encoding="utf-8") as file:
        file.writelines("Был создан пользователь с юзернейм "+ username +" "+ datetime.now().isoformat() + "\n")
    return RedirectResponse("/", status_code=303)  # 303 для POST->GET redirect
