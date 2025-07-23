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


@router.post("/", response_model=int)
async def crear(data: str = Form(...), db: AsyncSession = Depends(get_db), file: UploadFile = File(None)):
    
    if file:
        print(f"Recibido archivo: {file.filename}, tamaño: {file.size}")
    else:
        print("No se recibió archivo")

    try:
        # Parsear los datos JSON
        pub_data = json.loads(data)
        pub_data["FechaPublicacion"] = datetime.strptime(
            pub_data["FechaPublicacion"], 
            "%Y-%m-%d %H:%M:%S"
        )
        
        publication = PublicacionCreate(**pub_data)
        post = await crud.create(db, publication)
        
        if not post:
            raise HTTPException(status_code=400, detail="Error al crear la publicación")
        
        if file:
            # Obtener la ruta absoluta del directorio base del proyecto
            BASE_DIR = Path(__file__).resolve().parent.parent.parent
            IMAGE_DIR = BASE_DIR / "static" / "imagenes" / "publicaciones"
            
            # Crear directorio si no existe
            IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            
            # Generar nombre de archivo único
            file_extension = Path(file.filename).suffix
            filename = f"img_pub_{post.Id}_user{post.id_Usuario}_{post.FechaPublicacion}{file_extension}"
            file_path = IMAGE_DIR / filename
            
            # Guardar la imagen
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            # Actualizar la publicación con el nombre de la imagen
            post.Imagen = filename
            await db.commit()
            await db.refresh(post)
            
            print(f"Imagen guardada en: {file_path}")  # Para depuración
        
        return post.Id
        
    except Exception as e:
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
