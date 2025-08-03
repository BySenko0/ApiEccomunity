from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.recoleccion_usuario import RecoleccionCreate, RecoleccionUpdate, RecoleccionOut, StatusUpdate
from app.crud import recoleccion_usuario as crud

router = APIRouter(prefix="/recolecciones", tags=["Recolecciones de Usuarios"])

@router.get("/", response_model=list[RecoleccionOut])
async def listar_recolecciones(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_recolecciones(db)

@router.get("/{reco_id}", response_model=RecoleccionOut)
async def obtener_recoleccion(reco_id: int, db: AsyncSession = Depends(get_db)):
    reco = await crud.get_recoleccion_by_id(db, reco_id)
    if not reco:
        raise HTTPException(status_code=404, detail="Recolección no encontrada")
    return reco

@router.get("/usuario/{usuario_id}", response_model=list[RecoleccionOut])
async def obtener_recolecciones_por_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    reco = await crud.get_recolecciones_by_usuario(db, usuario_id)
    if not reco:
        return []
    return reco

@router.post("/actualizar-estatus/{reco_id}", response_model=bool)
async def actualizar_estatus_recoleccion(reco_id: int, status_update: StatusUpdate, db: AsyncSession = Depends(get_db)):
    reco = await crud.update_recoleccion_status(db, reco_id, status_update.nuevo_status)
    if not reco:
        raise HTTPException(status_code=404, detail="Recolección no encontrada")
    return True

@router.post("/", response_model=int)
async def crear_recoleccion(reco: RecoleccionCreate, db: AsyncSession = Depends(get_db)):
    reco = await crud.create_recoleccion(db, reco)
    return reco.Id

@router.put("/{reco_id}", response_model=RecoleccionOut)
async def actualizar_recoleccion(reco_id: int, reco: RecoleccionUpdate, db: AsyncSession = Depends(get_db)):
    actualizado = await crud.update_recoleccion(db, reco_id, reco)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Recolección no encontrada")
    return actualizado

@router.delete("/{reco_id}")
async def eliminar_recoleccion(reco_id: int, db: AsyncSession = Depends(get_db)):
    eliminado = await crud.delete_recoleccion(db, reco_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Recolección no encontrada")
    return {"ok": True, "mensaje": "Recolección eliminada correctamente"}
