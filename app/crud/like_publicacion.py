from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.likes_publicaciones import Likes_Publicaciones 
from app.schemas.like_publicacion import LikePublicacionCreate, LikePublicacionOut

async def get_all_likes_publicaciones(db: AsyncSession):
    result = await db.execute(select(Likes_Publicaciones))
    return result.scalars().all()

async def give_like_publicacion(db: AsyncSession, like_publicacion: LikePublicacionCreate):
    nuevo_like = Likes_Publicaciones(**like_publicacion.dict())
    db.add(nuevo_like)
    await db.commit()
    await db.refresh(nuevo_like)
    return nuevo_like

async def get_like_publicacion_by_user_and_post(db: AsyncSession, id_publicacion: int, id_usuario: int):
    result = await db.execute(
        select(Likes_Publicaciones).where(
            Likes_Publicaciones.id_Publicacion == id_publicacion,
            Likes_Publicaciones.id_Usuario == id_usuario
        )
    )

    like = result.scalar_one_or_none()
    if not like:
        return None

    await db.refresh(like)  # Asegurarse de que la instancia esté actualizada
    return like


async def remove_like_publicacion(db: AsyncSession, id_like):
    result = await db.execute(
        select(Likes_Publicaciones)
        .where(Likes_Publicaciones.Id == id_like)
    ) 
    
    like = result.scalar_one_or_none()  # Extraer la instancia
    
    if not like:
        return None
    
    await db.delete(like)
    await db.commit()
    return like

async def get_like_count_publicacion_(db: AsyncSession, id_publicacion: int):
    result = await db.execute(
        select(Likes_Publicaciones).where(Likes_Publicaciones.id_Publicacion == id_publicacion)
    )
    
    likes = result.scalars().all()
    return len(likes)
