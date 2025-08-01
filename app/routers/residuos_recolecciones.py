from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import residuos_recolecciones as crud
from app.schemas.residuos_recolecciones import ResiduoRecoleccionCreate, ResiduoRecoleccionOut

router = APIRouter(prefix="/residuos_recolecciones", tags=["Residuos Recolecciones"])

@router.post("/agregar", response_model=bool)
async def agregar_residuo_recoleccion(data: ResiduoRecoleccionCreate, db: AsyncSession = Depends(get_db)):
   
    nuevo_residuo = await crud.create(db, data)
    if not nuevo_residuo:
        raise HTTPException(status_code=400, detail="Error al agregar el residuo de recolección")
    return True