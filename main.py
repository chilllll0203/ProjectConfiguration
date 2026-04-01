from datetime import datetime
from fastapi import FastAPI, Request, Form, Depends
from sqlalchemy import ForeignKey, text , select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
import bcrypt
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Создание асинхронного движка и сессии
engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

templates = Jinja2Templates(directory="templates")

# Асинхронный генератор для работы с сессией
async def get_session() -> AsyncSession:
    async with async_session() as session:  # ВАЖНО: вызываем async_session()
        yield session

# Базовый класс моделей
class Base(DeclarativeBase):
    pass

# Модели
class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    role: Mapped[str]
    created_at: Mapped[datetime]

class EventModel(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    event_date: Mapped[datetime]
    type: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime]

class AchievementModel(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    category: Mapped[str]
    result: Mapped[str]
    document_url: Mapped[str]
    created_at: Mapped[datetime]

# Роуты
@app.get("/", summary="Вход")
def login_user(request: Request):
    return templates.TemplateResponse("extrance.html", {"request": request})

@app.get("/register", summary="Форма регистрации")
def get_form(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@app.post("/register", summary="Добавление пользователя")
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
    return RedirectResponse("/", status_code=303)  # 303 для POST->GET redirect

@app.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    # ORM-запрос возвращает объекты UserModel
    result = await session.execute(select(UserModel))
    users = result.scalars().all()  # scalars() превращает Result в объекты модели

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
