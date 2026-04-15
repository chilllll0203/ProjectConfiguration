from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import Base

# Создание асинхронного движка и сессии
engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)
