from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.centro_tiporeciclaje import CentroTipoReciclaje
from app.schemas.centro_tiporeciclaje import CentroTipoReciclajeOut, CentroTipoReciclajeCreate
from app.models.tipo_reciclaje import TipoReciclaje

async def obtener_tipos_reciclaje_por_punto(db: AsyncSession, punto_id: int):
    query = (
        select(
            CentroTipoReciclaje.Id,
            CentroTipoReciclaje.IdCentroReciclaje,
            CentroTipoReciclaje.IdTipoReciclaje,
            CentroTipoReciclaje.PrecioPorKg,
            TipoReciclaje.Nombre.label("tipo_reciclaje_nombre"),
            )
        .where(CentroTipoReciclaje.IdCentroReciclaje == punto_id)
        .join(TipoReciclaje, CentroTipoReciclaje.IdTipoReciclaje == TipoReciclaje.Id)
    )
    result = await db.execute(query)
    tipos_reciclaje = result.mappings().all()
    
    return tipos_reciclaje

async def obtener_tipos_reciclaje(db: AsyncSession):
    query = (
        select(
            CentroTipoReciclaje.Id,
            CentroTipoReciclaje.IdCentroReciclaje,
            CentroTipoReciclaje.IdTipoReciclaje,
            CentroTipoReciclaje.PrecioPorKg,
            TipoReciclaje.Nombre.label("tipo_reciclaje_nombre"),
        )
        .join(TipoReciclaje, CentroTipoReciclaje.IdTipoReciclaje == TipoReciclaje.Id)
    )
    result = await db.execute(query)
    tipos_reciclaje = result.mappings().all()
    
    return tipos_reciclaje

async def create(db: AsyncSession, data: CentroTipoReciclajeCreate):

    query = (
        select(CentroTipoReciclaje)
        .where(
            CentroTipoReciclaje.IdCentroReciclaje == data.IdCentroReciclaje,
            CentroTipoReciclaje.IdTipoReciclaje == data.IdTipoReciclaje
        )
    )
    existing_tipo = await db.execute(query)
    existing_tipo = existing_tipo.scalars().all()

    if existing_tipo:
        return "exists"
        
    nuevo_tipo = CentroTipoReciclaje(**data.dict())
    db.add(nuevo_tipo)
    await db.commit()
    await db.refresh(nuevo_tipo)
    
    return nuevo_tipo

async def delete(db: AsyncSession, id: int):
    query = select(CentroTipoReciclaje).where(CentroTipoReciclaje.Id == id)
    result = await db.execute(query)
    tipo_reciclaje = result.scalar_one_or_none()
    
    if tipo_reciclaje:
        await db.delete(tipo_reciclaje)
        await db.commit()
        return True
    return False