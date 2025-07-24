from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Usuario
from app.schemas.usuario import UsuarioOut, UsuarioCreate, UsuarioUpdate, UsuarioLogin
from app.crud import usuario as crud


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_usuarios(db)

@router.get("/{usuario_id}", response_model=UsuarioOut)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await crud.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioOut)
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_usuario(db, usuario)

@router.post("/login", response_model=UsuarioOut| str)
async def login(usuario: UsuarioLogin, db: AsyncSession = Depends(get_db)):
    return await crud.login_usuario(db, usuario)

@router.put("/{usuario_id}", response_model=UsuarioOut)
async def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_db)):
    usuario_actualizado = await crud.update_usuario(db, usuario_id, usuario)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado

@router.delete("/{usuario_id}")
@router.post("/{usuario_id}/delete")  # acepta POST también
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await crud.delete_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"ok": True, "mensaje": "Usuario eliminado correctamente"}




