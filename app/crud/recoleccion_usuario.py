from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.recoleccion_usuario import RecoleccionUsuario
from app.schemas.recoleccion_usuario import RecoleccionCreate, RecoleccionUpdate
from app.models.punto_recoleccion import PuntoRecoleccion
from app.models.usuario import Usuario


async def get_all_recolecciones(db: AsyncSession):
    result = await db.execute(select(RecoleccionUsuario))
    return result.scalars().all()

async def get_recoleccion_by_id(db: AsyncSession, reco_id: int):

    query = (
        select(
            RecoleccionUsuario.Id,
            RecoleccionUsuario.Tipo,
            RecoleccionUsuario.Dia,
            RecoleccionUsuario.Hora,
            RecoleccionUsuario.Cantidad,
            RecoleccionUsuario.Status,
            RecoleccionUsuario.id_PuntoRecoleccion,
            RecoleccionUsuario.id_Usuario,
            PuntoRecoleccion.Nombre.label("PuntoRecoleccion"),
            PuntoRecoleccion.Ubicacion.label("DireccionPunto"),
            Usuario.Nombre.label("UsuarioNombre"),
            )
            .where(RecoleccionUsuario.Id == reco_id)
            .join(PuntoRecoleccion, RecoleccionUsuario.id_PuntoRecoleccion == PuntoRecoleccion.Id)
            .join(Usuario, RecoleccionUsuario.id_Usuario == Usuario.Id)
    )
    result = await db.execute(query)
    return result.first()

async def get_recolecciones_by_usuario(db: AsyncSession, usuario_id: int):
    query = (
        select(
            RecoleccionUsuario.Id,
            RecoleccionUsuario.Tipo,
            RecoleccionUsuario.Dia,
            RecoleccionUsuario.Hora,
            RecoleccionUsuario.Cantidad,
            RecoleccionUsuario.Status,
            RecoleccionUsuario.id_PuntoRecoleccion,
            RecoleccionUsuario.id_Usuario,
            PuntoRecoleccion.Nombre.label("PuntoRecoleccion"),
            PuntoRecoleccion.Ubicacion.label("DireccionPunto"),
            Usuario.Nombre.label("UsuarioNombre"),
            )
        .where(RecoleccionUsuario.id_Usuario == usuario_id)
        .join(PuntoRecoleccion, RecoleccionUsuario.id_PuntoRecoleccion == PuntoRecoleccion.Id)
        .join(Usuario, RecoleccionUsuario.id_Usuario == Usuario.Id)
        .order_by(RecoleccionUsuario.Dia.desc(), RecoleccionUsuario.Hora.desc()
        )
    )
    result = await db.execute(query)
    return result.mappings().all()

async def update_recoleccion_status(db: AsyncSession, reco_id: int, nuevo_status: str):
    reco = await db.execute(select(RecoleccionUsuario).where(RecoleccionUsuario.Id == reco_id))
    reco = reco.scalar_one_or_none()
    if reco:
        reco.Status = nuevo_status
        await db.commit()
        await db.refresh(reco)
        return reco
    return None

async def create_recoleccion(db: AsyncSession, reco: RecoleccionCreate):
    nueva = RecoleccionUsuario(**reco.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def update_recoleccion(db: AsyncSession, reco_id: int, data: RecoleccionUpdate):
    reco = await get_recoleccion_by_id(db, reco_id)
    if reco:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(reco, key, value)
        await db.commit()
        await db.refresh(reco)
    return reco

async def delete_recoleccion(db: AsyncSession, reco_id: int):
    reco = await get_recoleccion_by_id(db, reco_id)
    if reco:
        await db.delete(reco)
        await db.commit()
    return reco
