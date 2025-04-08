from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import ArgumentError
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no está definida. Verifica tus variables en Railway.")

print("🔧 DATABASE_URL en uso:", DATABASE_URL)

try:
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
except ArgumentError as e:
    print("❌ Error al crear el engine:", e)
    raise

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Esta es la función que necesitas importar
async def get_db():
    async with SessionLocal() as session:
        yield session
