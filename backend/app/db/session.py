from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

connect_args = {}
if settings.TESTING:
    connect_args["check_same_thread"] = False

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args=connect_args,
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
