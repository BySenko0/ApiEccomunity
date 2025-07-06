import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import ArgumentError

load_dotenv()

# 1. Intenta obtener DATABASE_URL directamente
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Si no está, construye desde las partes individuales
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "Ecommunity")

    DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Validación y notificación
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no está definida ni se pudo construir a partir de las variables.")

print("🔧 DATABASE_URL en uso:", DATABASE_URL)

# 4. Crear el motor asincrónico
try:
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
except ArgumentError as e:
    print("❌ Error al crear el engine:", e)
    raise

# 5. Declarar sesión y base
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 6. Función para obtener la sesión
async def get_db():
    async with SessionLocal() as session:
        yield session
