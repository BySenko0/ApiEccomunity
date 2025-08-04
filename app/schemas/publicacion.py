from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator, model_validator
from datetime import datetime
import os

class PublicacionBase(BaseModel):
    Titulo: str
    Contenido: Optional[str] = None
    Imagen: Optional[str] = None
    FechaPublicacion: Optional[datetime] = None
    id_Usuario: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PublicacionCreate(PublicacionBase):
    pass

class PublicacionUpdate(PublicacionBase):
    pass

class PublicacionOut(BaseModel):
    Id: int
    Titulo: str
    Contenido: Optional[str] = None
    Imagen: Optional[str] = None
    ImagenUrl: Optional[HttpUrl] = None
    ImagenPerfilUsuarioUrl: Optional[HttpUrl] = None
    FechaPublicacion: Optional[datetime] = None
    id_Usuario: Optional[int] = None
    NombreUsuario: Optional[str] = None

    @model_validator(mode='after')
    def construct_image_urls(self) -> 'PublicacionOut':
        if self.Imagen:
            APP_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
            STATIC_IMG_FILES_PATH = os.getenv("STATIC_IMG_FILES_PATH", "/static/imagenes")

            base_url = f'{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/publicaciones/'
            self.ImagenUrl = f"{base_url}{self.Imagen}"
        
        return self
    
    class Config:
        from_attributes = True
        json_encoders = {
            'HttpUrl': lambda v: str(v) if v else None,
            datetime: lambda v: v.isoformat()
        }