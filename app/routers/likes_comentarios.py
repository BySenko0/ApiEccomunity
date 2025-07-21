from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.like_comentario import LikeComentarioCreate, LikeComentarioOut
from app.crud import like_comentario as crud_likes_comentario

router = APIRouter(prefix="/likes", tags=["Likes de comentarios"])

@router.get("/comentarios/{id_publicacion}", response_model=list[LikeComentarioOut])
async def obtener_likes_comentarios(id_publicacion: int, db: AsyncSession = Depends(get_db)):
    return await crud_likes_comentario.get_all_likes_comentarios(db, id_publicacion)

@router.get("/comentarios/{id_comentario}/usuario/{id_usuario}", response_model=LikeComentarioOut | bool)
async def verificar_like_comentario(id_comentario: int, id_usuario: int, db: AsyncSession = Depends(get_db)):
    like = await crud_likes_comentario.get_like_comentario_by_user_and_comment(db, id_comentario, id_usuario)
    if not like:
        return False
    return like

@router.post("/comentarios/dar_like/", response_model=bool)
async def dar_like_comentario(like: LikeComentarioCreate, db: AsyncSession = Depends(get_db)):
    result = await crud_likes_comentario.create_like_comentario(db, like)
    if not result:
        raise HTTPException(status_code=400, detail="Error al dar like al comentario")
    return True

@router.delete("/comentarios/quitar_like/{id_like}", response_model=bool)
async def quitar_like_comentario(id_like: int, db: AsyncSession = Depends(get_db)):
    like = await crud_likes_comentario.remove_like_comment(db, id_like)
    if not like:
        raise HTTPException(status_code=404, detail="Like no encontrado")
    return True
    