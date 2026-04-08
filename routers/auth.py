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

# Секретный ключ
router.add_middleware(SessionMiddleware, secret_key="secret")

# Шаблонизатор для загрузки html-страниц
templates = Jinja2Templates(directory="templates")

@router.get("/", summary="Форма входа")
def login_user(request: Request):
    return templates.TemplateResponse("extrance.html", {"request": request})
@router.post("/", summary="Вход в кабинет и проверка на совпадение пользователя")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    request.session["username"] = user.username
    if(user.username == username and bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8"))):
        if(user.role == "student"):
            return RedirectResponse("/person_account_student", status_code=303)
        elif(user.role == "teacher"):
            return RedirectResponse("/person_account_teacher", status_code=303)
        elif(user.role == "administrator"):
            return RedirectResponse("/person_account_administrator", status_code=303)
        else:
            return "Произошла ошибка попробуйте снова!"

@router.get("/register", summary="Форма регистрации")
def get_form(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

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
