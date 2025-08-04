from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.centro_tiporeciclaje import CentroTipoReciclajeOut, CentroTipoReciclajeCreate, CentroTipoReciclajeBase 
from app.crud import centro_tiporeciclaje as crud

router = APIRouter(prefix="/puntos/tipos-reciclaje", tags=["Puntos de Recoleccion - Tipos de Reciclaje"])

@router.get("/todos", response_model=list[CentroTipoReciclajeOut])
async def obtener_tipos_reciclaje_de_puntos(db: AsyncSession = Depends(get_db)):
    tipos_reciclaje = await crud.obtener_tipos_reciclaje(db)
    if not tipos_reciclaje:
        return []
    return tipos_reciclaje

@router.get("/{punto_id}", response_model=list[CentroTipoReciclajeOut])
async def obtener_tipos_reciclaje_por_punto(punto_id: int, db: AsyncSession = Depends(get_db)):
    tipos_reciclaje = await crud.obtener_tipos_reciclaje_por_punto(db, punto_id)
    if not tipos_reciclaje:
        return []
    
    return tipos_reciclaje


@router.post("/agregar", response_model=bool)
async def agregar_tipo_reciclaje( data: CentroTipoReciclajeCreate, db: AsyncSession = Depends(get_db)):
    nuevo_tipo = CentroTipoReciclajeBase(**data.dict())
    nuevo_tipo = await crud.create(db, nuevo_tipo)
    if not nuevo_tipo:
        raise HTTPException(status_code=400, detail="Error al crear el tipo de reciclaje")
    elif nuevo_tipo == "exists":
        raise HTTPException(status_code=400, detail="El tipo de reciclaje ya existe para este punto de recolección")
    return True


@router.delete("/{id}", response_model=bool)
async def eliminar_tipo_reciclaje(id: int, db: AsyncSession = Depends(get_db)):
    response = await crud.delete(db, id)
    if not response:
        raise HTTPException(status_code=404, detail="Tipo de reciclaje no encontrado")
    return True