from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.comentario import ComentarioCreate, ComentarioUpdate, ComentarioOut
from app.crud import comentario as crud

from typing import Dict

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])


@router.get("/count", response_model=Dict[int, int])
async def comentarios_count_por_publicacion(db: AsyncSession = Depends(get_db)):
    return await crud.comments_count_by_posts(db)


@router.get("/", response_model=list[ComentarioOut])
async def listar(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)

@router.get("/{comentario_id}", response_model=ComentarioOut)
async def obtener(comentario_id: int, db: AsyncSession = Depends(get_db)):
    dato = await crud.get_by_id(db, comentario_id)
    if not dato:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return dato

@router.post("/", response_model=ComentarioOut)
async def crear(data: ComentarioCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create(db, data)

@router.put("/{comentario_id}", response_model=ComentarioOut)
async def actualizar(comentario_id: int, data: ComentarioUpdate, db: AsyncSession = Depends(get_db)):
    actualizado = await crud.update(db, comentario_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return actualizado

@router.delete("/{comentario_id}")
async def eliminar(comentario_id: int, db: AsyncSession = Depends(get_db)):
    eliminado = await crud.delete(db, comentario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {"ok": True, "mensaje": "Comentario eliminado correctamente"}

@router.get("/comentarios_publicacion/{publicacion_id}", response_model=list[ComentarioOut])
async def comentarios_por_publicacion(publicacion_id: int, db: AsyncSession = Depends(get_db)):
    comentarios = await crud.get_by_publicacion(db, publicacion_id)
    if not comentarios:
        return []
    return comentarios
