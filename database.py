from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy import ForeignKey, text , select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


# Создание асинхронного движка и сессии
DATABASE_URL = "postgresql://postgres_projectconfiguration_user:acfTXKyGRhtVXIBhDCCJnkUQCG3Qrpwu@dpg-d7fnofd8nd3s73e196d0-a.virginia-postgres.render.com/postgres_projectconfiguration"

engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

router = APIRouter()

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


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return "База данных создана"
