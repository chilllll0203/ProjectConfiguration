from sqlalchemy import ForeignKey, text , select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

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

class TelegramAuthenticationModel(Base):
    __tablename__ = "telegram_authentication"
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"),primary_key=True)
    telegramId: Mapped[int] = mapped_column(primary_key=True)