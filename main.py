from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from pydantic import BaseModel
import bcrypt
from alembic import op
from openpyxl import Workbook, load_workbook

app = FastAPI()
engine = create_async_engine('sqlite+aiosqlite:///database.db')

new_session = async_sessionmaker(engine, expire_on_commit=False) # создание сессии


async def get_session(): # метод для удобной работы с sqlalchemy
    async with new_session as session:
        yield session

class Base(DeclarativeBase): # пустой класс от которого будет наследоваться пользовательская модель и тд.
    pass

class Role(Base):# модель таблицы ролей пользователей
    __tablename__ = "roles"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    description:Mapped[str]

class UserModel(Base): # модель таблицы пользователи
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str]
    email:Mapped[str]
    hashed_password:Mapped[str]
    role:Mapped[int] = mapped_column(ForeignKey("roles.id"))
    created_at:Mapped[datetime]

class EventModel(Base):# модель таблицы мероприятия
    __tablename__ = "events"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str]
    description:Mapped[str]
    event_date:Mapped[datetime]
    type:Mapped[str]
    created_by:Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime]

class AchievementModel(Base):# модель таблицы достижений
    __tablename__ = "achievements"
    id:Mapped[int] = mapped_column(primary_key=True)
    student_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id:Mapped[int] = mapped_column(ForeignKey("events.id"))
    category:Mapped[str]
    result:Mapped[str]
    document_url:Mapped[str]
    created_at:Mapped[datetime]

@app.get("/", summary = "Главная страница")
def root():
    return "Hello World"
@app.post("/register",summary = "Регистрация")
def register_user():
    return "Регистрация пользователя"
@app.post("/login",summary = "Вход")
def register_user():
    return "Вход пользователя"
@app.post("/setup_database",summary = "Создание базы данных")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok":True}