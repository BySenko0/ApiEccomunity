from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.comentario import Comentario
from app.schemas.comentario import ComentarioCreate, ComentarioUpdate

from sqlalchemy import func

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
    result = await db.execute(select(Comentario).where(Comentario.id_Publicacion == publicacion_id))
    return result.scalars().all()


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