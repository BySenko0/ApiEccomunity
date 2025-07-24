from pydantic import BaseModel, HttpUrl
from datetime import datetime as date
from typing import Optional

class ComentarioBase(BaseModel):
    Texto: str
    Fecha: date
    id_Publicacion: int
    id_Usuario: int

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioUpdate(ComentarioBase):
    pass

class ComentarioOut(ComentarioBase):
    Id: int
    NombreUsuario: str
    ImagenPerfilUsuario: Optional[str] = None  # Nombre del archivo de imagen
    ImagenPerfilUsuarioUrl: Optional[HttpUrl] = None  # URL completa de la imagen
    
    class Config:
        orm_mode = True
        json_encoders = {
            'HttpUrl': lambda v: str(v) if v else None,
            'date': lambda v: v.isoformat()
        }