from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.tipo_reciclaje import TipoReciclaje
from app.schemas.tipo_reciclaje import TipoReciclajeCreate, TipoReciclajeUpdate

async def get_all_tipos(db: AsyncSession):
    result = await db.execute(select(TipoReciclaje))
    return result.scalars().all()

async def get_tipo_by_id(db: AsyncSession, tipo_id: int):
    result = await db.execute(
        select(TipoReciclaje).where(TipoReciclaje.Id == tipo_id)
    )
    return result.scalar_one_or_none()

async def create_tipo(db: AsyncSession, tipo_data: TipoReciclajeCreate):
    # Crear instancia del modelo con los datos proporcionados
    nuevo_tipo = TipoReciclaje(
        Nombre=tipo_data.nombre,
        PesoMinimo=tipo_data.peso_minimo,
        PesoMaximo=tipo_data.peso_maximo,
        PagoPorKg=tipo_data.pago_por_kg,
        GananciaPorKg=tipo_data.ganancia_por_kg,
        FechaCreacion=tipo_data.fecha_creacion
    )
    db.add(nuevo_tipo)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # Posible violación de UNIQUE (nombre duplicado)
        raise HTTPException(status_code=400, detail="Nombre ya existe")
    await db.refresh(nuevo_tipo)
    return nuevo_tipo

async def update_tipo(db: AsyncSession, tipo_id: int, tipo_data: TipoReciclajeUpdate):
    tipo = await get_tipo_by_id(db, tipo_id)
    if not tipo:
        return None
    # Actualizar solo los campos provistos (no None)
    if tipo_data.nombre is not None:
        tipo.Nombre = tipo_data.nombre
    if tipo_data.peso_minimo is not None:
        tipo.PesoMinimo = tipo_data.peso_minimo
    if tipo_data.peso_maximo is not None:
        tipo.PesoMaximo = tipo_data.peso_maximo
    if tipo_data.pago_por_kg is not None:
        tipo.PagoPorKg = tipo_data.pago_por_kg
    if tipo_data.ganancia_por_kg is not None:
        tipo.GananciaPorKg = tipo_data.ganancia_por_kg
    if tipo_data.fecha_creacion is not None:
        tipo.FechaCreacion = tipo_data.fecha_creacion
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # Posible violación de UNIQUE (nombre duplicado)
        raise HTTPException(status_code=400, detail="Nombre ya existe")
    await db.refresh(tipo)
    return tipo

async def delete_tipo(db: AsyncSession, tipo_id: int):
    tipo = await get_tipo_by_id(db, tipo_id)
    if not tipo:
        return None
    try:
        await db.delete(tipo)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # Posible violación de FK: existen registros relacionados en otras tablas
        raise HTTPException(status_code=400, detail="No se puede eliminar el tipo, está en uso")
    return tipo
