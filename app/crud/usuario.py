# app/crud/usuario.py

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioLogin
from typing import Optional
import os

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def login_usuario(db: AsyncSession, usuario):
    result = await db.execute(
        select(Usuario).where(Usuario.Correo == usuario.correo)
    )
    usuario_db = result.scalar_one_or_none()
    
    if usuario_db and pwd_context.verify(usuario.contrasena, usuario_db.contrasena):
        return usuario_db
    else:
        return "Credenciales inválidas"

async def get_all_usuarios(db: AsyncSession) -> list[Usuario]:
    result = await db.execute(select(Usuario))
    return result.scalars().all()

async def get_usuario_by_id(db: AsyncSession, usuario_id: int) -> Optional[UsuarioOut]:
    result = await db.execute(
        select(Usuario).where(Usuario.Id == usuario_id)
    )
    usuario = result.scalar_one_or_none()
    
    if usuario:
        # Convertir a diccionario para poder añadir las URLs
        usuario_dict = usuario.__dict__
        
        APP_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
        STATIC_IMG_FILES_PATH = os.getenv("STATIC_IMG_FILES_PATH", "/static/imagenes")

        # Añadir URL de imagen de perfil
        if usuario_dict.get('Imagen_perfil'):
            usuario_dict['ImagenPerfilUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/perfil/{usuario_dict['Imagen_perfil']}"
        else:
            usuario_dict['ImagenPerfilUrl'] = None
            
        # Añadir URL de imagen de fondo
        if usuario_dict.get('Imagen_fondo'):
            usuario_dict['ImagenFondoUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/fondo/{usuario_dict['Imagen_fondo']}"
        else:
            usuario_dict['ImagenFondoUrl'] = None
            
        return UsuarioOut(**usuario_dict)
    
    return None

async def create_usuario(db: AsyncSession, usuario: UsuarioCreate) -> Usuario:
    try:
        nuevo_usuario = Usuario(
            Nombre=usuario.nombre,
            Correo=usuario.correo,
            contrasena=hash_password(usuario.contrasena),
            Ubicacion=usuario.ubicacion,
            Rol=usuario.rol,
            Estado=usuario.estado,
            Cooldown=usuario.cooldown,
            url_perfil=usuario.url_perfil,
            Imagen_perfil=usuario.imagen_perfil,
            Imagen_fondo=usuario.imagen_fondo
        )
        db.add(nuevo_usuario)
        await db.commit()
        await db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        await db.rollback()
        raise e

async def update_usuario(
    db: AsyncSession,
    usuario_id: int,
    usuario_data: UsuarioUpdate
) -> Usuario | None:
    # Obtener instancia ORM directamente
    result = await db.execute(select(Usuario).where(Usuario.Id == usuario_id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        return None

    field_map = {
        "nombre": "Nombre",
        "ubicacion": "Ubicacion",
        "rol": "Rol",
        "estado": "Estado",
        "cooldown": "Cooldown",
        "url_perfil": "url_perfil",
        "imagen_perfil": "Imagen_perfil",
        "imagen_fondo": "Imagen_fondo",
    }
    data = usuario_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(usuario, field_map[key], value)

    await db.commit()
    await db.refresh(usuario)
    return usuario

async def delete_usuario(db: AsyncSession, usuario_id: int):
    result = await db.execute(select(Usuario).where(Usuario.Id == usuario_id))
    usuario_db = result.scalar_one_or_none()

    if usuario_db is None:
        return None  # El endpoint manejará el 404

    await db.delete(usuario_db)
    await db.commit()
    return usuario_db
