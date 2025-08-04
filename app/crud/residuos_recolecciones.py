from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.residuos_recolecciones import ResiduosRecolecciones
from app.schemas.residuos_recolecciones import ResiduoRecoleccionCreate, ResiduoRecoleccionOut
from app.models.centro_tiporeciclaje import CentroTipoReciclaje
from app.models.tipo_reciclaje import TipoReciclaje

async def create(db: AsyncSession, data: ResiduoRecoleccionCreate) -> bool:
    
    nueva = ResiduosRecolecciones(**data.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def get_by_recoleccion_id(db: AsyncSession, recoleccion_id: int) -> list[ResiduoRecoleccionOut]:
    query = (
        select(
            ResiduosRecolecciones.Id,
            ResiduosRecolecciones.Cantidad,
            ResiduosRecolecciones.IdRecoleccionUsuario,
            ResiduosRecolecciones.IdTipoReciclajeCentro,
            TipoReciclaje.Nombre.label("NombreTipoReciclaje")
            )
        .where(ResiduosRecolecciones.IdRecoleccionUsuario == recoleccion_id)
        .join(CentroTipoReciclaje, ResiduosRecolecciones.IdTipoReciclajeCentro == CentroTipoReciclaje.Id)
        .join(TipoReciclaje, CentroTipoReciclaje.IdTipoReciclaje == TipoReciclaje.Id)   
    )
    result = await db.execute(query)
    return result.fetchall()   