from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Создание асинхронного движка и сессии
DATABASE_URL = "postgresql://postgres_projectconfiguration_user:acfTXKyGRhtVXIBhDCCJnkUQCG3Qrpwu@dpg-d7fnofd8nd3s73e196d0-a.virginia-postgres.render.com/postgres_projectconfiguration"

engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

