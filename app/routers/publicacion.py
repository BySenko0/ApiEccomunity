# FastAPI core imports
from fastapi import APIRouter, Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Database related imports
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Schemas and CRUD operations
from app.schemas.publicacion import PublicacionCreate, PublicacionOut, PublicacionUpdate
from app.crud import publicacion as crud

# Standard library and utilities
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional



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

@router.get("/por/{user_id}", response_model=list[PublicacionOut])
async def obtener_por_usuario(user_id: int, db: AsyncSession = Depends(get_db)):
    publicaciones = await crud.get_by_user_id(db, user_id)
    if not publicaciones:
        return []
    return publicaciones

@router.post("/", response_model=int)
async def crear(
    data: str = Form(...),
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(None),
):

    if file:
        print(f"Recibido archivo: {file.filename}, tamaño: {file.size}")
    else:
        print("No se recibió archivo")

    try:
        # 1) Parsear JSON y convertir fecha a datetime
        pub_data = json.loads(data)
        pub_data["FechaPublicacion"] = datetime.strptime(
            pub_data["FechaPublicacion"], "%Y-%m-%d %H:%M:%S"
        )

        # 2) Validar/crear la publicación en BD
        publication = PublicacionCreate(**pub_data)
        post = await crud.create(db, publication)
        if not post:
            raise HTTPException(status_code=400, detail="Error al crear la publicación")

        # 3) Si hay archivo, guardarlo en disco y actualizar el registro
        if file:
            BASE_DIR = Path(__file__).resolve().parent.parent.parent
            IMAGE_DIR = BASE_DIR / "static" / "imagenes" / "publicaciones"
            IMAGE_DIR.mkdir(parents=True, exist_ok=True)

            # Generar un timestamp seguro para Windows: no usar ':'
            ts = post.FechaPublicacion.strftime("%Y-%m-%d_%H-%M-%S")
            ext = Path(file.filename).suffix  # .jpg, .png, etc.
            filename = f"img_pub_{post.Id}user{post.id_Usuario}{ts}{ext}"
            file_path = IMAGE_DIR / filename

            # Escribir el binario
            contents = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(contents)

            # Actualizar el campo Imagen en la BD
            post.Imagen = filename
            await db.commit()
            await db.refresh(post)

            print(f"Imagen guardada en: {file_path}")

        return post.Id

    except HTTPException:
        # Re-lanzar HTTPExceptions sin envolver
        raise
    except Exception as e:
        # Cualquier otro error -> 500
        print("Error al crear publicación:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
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
