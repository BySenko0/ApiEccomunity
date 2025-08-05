from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Usuario
from app.schemas.usuario import UsuarioOut, UsuarioCreate, UsuarioUpdate, UsuarioLogin
from app.crud import usuario as crud

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Usuario
from app.schemas.usuario import UsuarioOut, UsuarioCreate, UsuarioUpdate, UsuarioLogin
from app.crud import usuario as crud
from pathlib import Path
import os
from datetime import datetime
from fastapi import APIRouter, Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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


@router.post("/{usuario_id}/imagen-perfil", response_model=UsuarioOut)
async def actualizar_imagen_perfil(
    usuario_id: int, 
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Verificar que el usuario existe
    result = await db.execute(select(Usuario).where(Usuario.Id == usuario_id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        # Configurar directorios
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        IMAGE_DIR = BASE_DIR / "static" / "imagenes" / "perfil"
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)

        # Generar nombre único para la imagen
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        ext = Path(file.filename).suffix
        filename = f"perfil_{usuario_id}_{ts}{ext}"
        file_path = IMAGE_DIR / filename

        # Guardar la imagen
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # Actualizar la base de datos
        usuario.Imagen_perfil = filename
        await db.commit()
        await db.refresh(usuario)

        return usuario

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar imagen de perfil: {str(e)}")

@router.post("/{usuario_id}/imagen-fondo", response_model=UsuarioOut)
async def actualizar_imagen_fondo(
    usuario_id: int, 
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Verificar que el usuario existe
    result = await db.execute(select(Usuario).where(Usuario.Id == usuario_id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        # Configurar directorios
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        IMAGE_DIR = BASE_DIR / "static" / "imagenes" / "fondo"
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)

        # Generar nombre único para la imagen
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        ext = Path(file.filename).suffix
        filename = f"fondo_{usuario_id}_{ts}{ext}"
        file_path = IMAGE_DIR / filename

        # Guardar la imagen
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # Actualizar la base de datos
        usuario.Imagen_fondo = filename
        await db.commit()
        await db.refresh(usuario)

        return usuario

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar imagen de fondo: {str(e)}")