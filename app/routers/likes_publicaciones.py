from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.like_publicacion import LikePublicacionCreate, LikePublicacionOut
from app.crud import like_publicacion as crud_likes_publicacion


router = APIRouter(prefix="/likes", tags=["Likes de publicaciones"])

@router.get("/publicaciones", response_model=list[LikePublicacionOut])
async def obtener_likes_publicaciones(db: AsyncSession = Depends(get_db)):
    return await crud_likes_publicacion.get_all_likes_publicaciones(db)

@router.get("/publicaciones/count/{id_publicacion}", response_model=int)
async def contar_likes_publicacion(id_publicacion: int, db: AsyncSession = Depends(get_db)):
    likes = await crud_likes_publicacion.get_like_count_publicacion_(db, id_publicacion)
    return likes

@router.get("/publicaciones/{id_publicacion}/usuario/{id_usuario}", response_model=LikePublicacionOut | None)
async def obtener_like_publicacion(id_publicacion: int, id_usuario: int, db: AsyncSession = Depends(get_db)):
    like = await crud_likes_publicacion.get_like_publicacion_by_user_and_post(db, id_publicacion, id_usuario)
    if not like:
        return None
    
    return like


@router.post("/publicaciones/dar_like/", response_model=LikePublicacionOut)
async def dar_like_publicacion(data: LikePublicacionCreate, db: AsyncSession = Depends(get_db)):
    return await crud_likes_publicacion.give_like_publicacion(db, data)

@router.delete("/publicaciones/quitar_like/{id_like}")
# @router.post("/publicaciones/{id_like}/quitar_like")
async def quitar_like(id_like: int, db: AsyncSession = Depends(get_db)):
    like = await crud_likes_publicacion.remove_like_publicacion(db, id_like)
    if not like:
        raise HTTPException(status_code=404, detail="Like no encontrado")
    return {"ok": True, "mensaje": "Like eliminado correctamente"}

