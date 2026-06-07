from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings


engine = create_async_engine(url=settings.db.url, echo=settings.db.echo)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
AsyncSessionLocalRR = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    execution_options={"isolation_level": "REPEATABLE READ"}
)

class Base(DeclarativeBase):
    ...

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

async def get_db_rr():
    async with AsyncSessionLocalRR() as db:
        yield db

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
