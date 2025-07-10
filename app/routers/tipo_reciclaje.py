from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.tipo_reciclaje import (
    TipoReciclajeCreate, TipoReciclajeUpdate, TipoReciclajeOut
)
from app.crud import tipo_reciclaje as crud

router = APIRouter(prefix="/tipos-reciclaje", tags=["Tipos de Reciclaje"])

@router.get("/", response_model=list[TipoReciclajeOut])
async def listar_tipos(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_tipos(db)

@router.get("/{tipo_id}", response_model=TipoReciclajeOut)
async def obtener_tipo(tipo_id: int, db: AsyncSession = Depends(get_db)):
    tipo = await crud.get_tipo_by_id(db, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return tipo

@router.post("/", response_model=TipoReciclajeOut)
async def crear_tipo(tipo: TipoReciclajeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_tipo(db, tipo)

@router.put("/{tipo_id}", response_model=TipoReciclajeOut)
async def actualizar_tipo(tipo_id: int, tipo: TipoReciclajeUpdate, db: AsyncSession = Depends(get_db)):
    actualizado = await crud.update_tipo(db, tipo_id, tipo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return actualizado

@router.delete("/{tipo_id}")
async def eliminar_tipo(tipo_id: int, db: AsyncSession = Depends(get_db)):
    eliminado = await crud.delete_tipo(db, tipo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return {"ok": True, "mensaje": "Tipo eliminado correctamente"}
