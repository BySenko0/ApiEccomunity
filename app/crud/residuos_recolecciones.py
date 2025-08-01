from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.residuos_recolecciones import ResiduosRecolecciones
from app.schemas.residuos_recolecciones import ResiduoRecoleccionCreate, ResiduoRecoleccionOut


async def create(db: AsyncSession, data: ResiduoRecoleccionCreate) -> bool:
    
    nueva = ResiduosRecolecciones(**data.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva