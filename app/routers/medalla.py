from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.medalla import Medalla
from app.schemas.medalla import MedallaCreate, MedallaOut

router = APIRouter(prefix="/medallas", tags=["Medallas"])

@router.get("/", response_model=list[MedallaOut])
async def listar_medallas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medalla))
    return result.scalars().all()

@router.post("/", response_model=MedallaOut)
async def crear_medalla(medalla: MedallaCreate, db: AsyncSession = Depends(get_db)):
    nueva = Medalla(**medalla.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

@router.get("/{medalla_id}", response_model=MedallaOut)
async def obtener_medalla(medalla_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medalla).where(Medalla.id == medalla_id))
    medalla = result.scalar_one_or_none()
    if not medalla:
        raise HTTPException(status_code=404, detail="Medalla no encontrada")
    return medalla

@router.put("/{medalla_id}", response_model=MedallaOut)
async def actualizar_medalla(medalla_id: int, data: MedallaCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medalla).where(Medalla.id == medalla_id))
    medalla = result.scalar_one_or_none()
    if not medalla:
        raise HTTPException(status_code=404, detail="Medalla no encontrada")

    for key, value in data.dict().items():
        setattr(medalla, key, value)

    await db.commit()
    await db.refresh(medalla)
    return medalla

@router.delete("/{medalla_id}")
async def eliminar_medalla(medalla_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Medalla).where(Medalla.id == medalla_id))
    medalla = result.scalar_one_or_none()
    if not medalla:
        raise HTTPException(status_code=404, detail="Medalla no encontrada")

    await db.delete(medalla)
    await db.commit()
    return {"ok": True, "mensaje": "Medalla eliminada correctamente"}
