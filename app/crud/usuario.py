# app/crud/usuario.py

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def get_all_usuarios(db: AsyncSession) -> list[Usuario]:
    result = await db.execute(select(Usuario))
    return result.scalars().all()

async def get_usuario_by_id(db: AsyncSession, usuario_id: int) -> Usuario | None:
    result = await db.execute(
        select(Usuario).where(Usuario.Id == usuario_id)
    )
    return result.scalar_one_or_none()

async def create_usuario(db: AsyncSession, usuario: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(
        Nombre=usuario.nombre,
        Correo=usuario.correo,
        contrasena=hash_password(usuario.contrasena),
        Ubicacion=usuario.ubicacion,
        Rol=usuario.rol,
        Estado=usuario.estado,
        Cooldown=usuario.cooldown,
        url_perfil=usuario.url_perfil
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

async def update_usuario(
    db: AsyncSession,
    usuario_id: int,
    usuario_data: UsuarioUpdate
) -> Usuario | None:
    usuario = await get_usuario_by_id(db, usuario_id)
    if not usuario:
        return None

    # Mapeo de campos pydantic -> atributos SQLAlchemy
    field_map = {
        "nombre": "Nombre",
        "ubicacion": "Ubicacion",
        "rol": "Rol",
        "estado": "Estado",
        "cooldown": "Cooldown",
        "url_perfil": "url_perfil",
    }
    data = usuario_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(usuario, field_map[key], value)

    await db.commit()
    await db.refresh(usuario)
    return usuario

async def delete_usuario(db: AsyncSession, usuario_id: int) -> Usuario | None:
    usuario = await get_usuario_by_id(db, usuario_id)
    if not usuario:
        return None

    await db.delete(usuario)
    await db.commit()
    return usuario
