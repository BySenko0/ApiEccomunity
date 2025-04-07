import pymysql
import asyncio
import os
from dotenv import load_dotenv
from app.database import engine, Base
from app import models  

load_dotenv()

def create_database():
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": int(os.getenv("DB_PORT"))
    }
    db_name = os.getenv("DB_NAME")

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"✅ Base de datos `{db_name}` verificada/creada.")
    cursor.close()
    conn.close()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    create_database()
    asyncio.run(create_tables())
