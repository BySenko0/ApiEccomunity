from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.likes_comentarios import Likes_Comentarios
from app.models.comentario import Comentario
from app.schemas.like_comentario import LikeComentarioCreate, LikeComentarioOut

async def get_all_likes_comentarios(db: AsyncSession, id_publicacion: int):
    query = (
        select(Likes_Comentarios)
        .join(Comentario, Likes_Comentarios.id_Comentario == Comentario.Id)
        .where(Comentario.id_Publicacion == id_publicacion)
    )
    result = await db.execute(query)
    if not result:
        return []
    return result.scalars().all()

async def create_like_comentario(db: AsyncSession, like: LikeComentarioCreate):
    nuevo_like = Likes_Comentarios(**like.dict())
    db.add(nuevo_like)
    await db.commit()
    await db.refresh(nuevo_like)
    return nuevo_like

async def get_like_comentario_by_user_and_comment(db: AsyncSession, id_comentario: int, id_usuario: int):
    result = await db.execute(
        select(Likes_Comentarios).where(
            Likes_Comentarios.id_Comentario == id_comentario,
            Likes_Comentarios.id_Usuario == id_usuario
        )
    )
    like = result.scalars().first()
    if not like:
        return None
    await db.refresh(like)
    return like

async def remove_like_comment(db: AsyncSession, id_comentario):
    like = await db.execute(
        select(Likes_Comentarios)
        .where(Likes_Comentarios.Id == id_comentario)
    )
    like = like.scalar_one_or_none()
    if not like:
        return None
    await db.delete(like)
    await db.commit()
    return like

