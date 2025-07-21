from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate, PublicacionOut
from app.crud import publicacion as crud

router = APIRouter(prefix="/publicaciones", tags=["Publicaciones"])

@router.get("/", response_model=list[PublicacionOut])
async def listar(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.get("/{pub_id}", response_model=PublicacionOut)
async def obtener(pub_id: int, db: AsyncSession = Depends(get_db)):
    dato = await crud.get_by_id(db, pub_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return dato

@router.post("/", response_model=bool)
async def crear(data: PublicacionCreate, db: AsyncSession = Depends(get_db)):
    post = await crud.create(db, data)
    if not post:
        raise HTTPException(status_code=400, detail="Error al crear la publicación")
    return True

@router.put("/{pub_id}", response_model=PublicacionOut)
async def actualizar(pub_id: int, data: PublicacionUpdate, db: AsyncSession = Depends(get_db)):
    actualizado = await crud.update(db, pub_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return actualizado

@router.delete("/{pub_id}")
async def eliminar(pub_id: int, db: AsyncSession = Depends(get_db)):
    eliminado = await crud.delete(db, pub_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return {"ok": True, "mensaje": "Publicación eliminada correctamente"}
