from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    empresa, likes_publicaciones, usuario, punto_recoleccion, horario_recoleccion,
    recoleccion_usuario, tipo_reciclaje, empresa_tiporeciclaje,
    recoleccion_empresa, publicacion, comentario, bitacora, medalla, usuario_medalla, likes_comentarios, centro_tiporeciclaje, residuos_recolecciones
)
from create_db_and_tables import create_tables  # Eliminamos create_database

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="API de Recolección")

UPLOAD_DIR = "static/imagenes"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todos los routers
app.include_router(empresa.router)
app.include_router(usuario.router)
app.include_router(punto_recoleccion.router)
app.include_router(horario_recoleccion.router)
app.include_router(recoleccion_usuario.router)
app.include_router(tipo_reciclaje.router)
app.include_router(empresa_tiporeciclaje.router)
app.include_router(recoleccion_empresa.router)
app.include_router(publicacion.router)
app.include_router(comentario.router)
app.include_router(bitacora.router)
app.include_router(medalla.router)
app.include_router(usuario_medalla.router)
app.include_router(likes_publicaciones.router)
app.include_router(likes_comentarios.router)
app.include_router(centro_tiporeciclaje.router)
app.include_router(residuos_recolecciones.router)

@app.on_event("startup")
async def startup_event():
    try:
        print("🚀 Ejecutando create_tables()...")
        await create_tables()
        print("✅ Startup exitoso.")
    except Exception as e:
        print("❌ Error durante startup:", str(e))
        raise

@app.get("/")
async def root():
    return {"mensaje": "Bienvenido a la API de recolección"}
