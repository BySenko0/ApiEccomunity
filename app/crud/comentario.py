from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.comentario import Comentario
from app.models.usuario import Usuario
from app.schemas.comentario import ComentarioCreate, ComentarioUpdate
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func
import os

async def get_all(db: AsyncSession):
    result = await db.execute(select(Comentario))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, comentario_id: int):
    result = await db.execute(select(Comentario).where(Comentario.Id == comentario_id))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, data: ComentarioCreate):
    nuevo = Comentario(**data.dict())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo

async def update(db: AsyncSession, comentario_id: int, data: ComentarioUpdate):
    comentario = await get_by_id(db, comentario_id)
    if comentario:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(comentario, key, value)
        await db.commit()
        await db.refresh(comentario)
    return comentario

async def delete(db: AsyncSession, comentario_id: int):
    comentario = await get_by_id(db, comentario_id)
    if comentario:
        await db.delete(comentario)
        await db.commit()
    return comentario


async def get_by_publicacion(db: AsyncSession, publicacion_id: int):
    query = (
        select(
            Comentario.Id,
            Comentario.Texto,
            Comentario.Fecha,
            Comentario.id_Publicacion,
            Comentario.id_Usuario,
            Usuario.Nombre.label("NombreUsuario"),
            Usuario.Imagen_perfil.label("ImagenPerfilUsuario")  # Nuevo campo añadido
        )
        .join(Usuario, Comentario.id_Usuario == Usuario.Id)
        .where(Comentario.id_Publicacion == publicacion_id)
        .order_by(Comentario.Fecha.desc())
    )
    
    result = await db.execute(query)
    comentarios = result.mappings().all()
    
    # Convertir RowMapping a dict y añadir URL de imagen de perfil
    comentarios_con_url = []
    for comentario in comentarios:

        comentario_dict = dict(comentario)

        APP_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
        STATIC_IMG_FILES_PATH = os.getenv("STATIC_FILES_PATH", "/static/imagenes")

        # Añadir URL de la imagen de perfil del usuario
        if comentario_dict['ImagenPerfilUsuario']:
            comentario_dict['ImagenPerfilUsuarioUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/perfil/{comentario_dict['ImagenPerfilUsuario']}"
        else:
            comentario_dict['ImagenPerfilUsuarioUrl'] = None

        comentarios_con_url.append(comentario_dict)
    
    return comentarios_con_url

async def comments_count_by_posts(db: AsyncSession):
    stmt = (
        select(
            Comentario.id_Publicacion,
            func.count(Comentario.Id).label("count")
        )
        .group_by(Comentario.id_Publicacion)
    )
    
    result = await db.execute(stmt)
    
    return {row.id_Publicacion: row.count for row in result.all()}