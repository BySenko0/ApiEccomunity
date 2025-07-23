from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PublicacionBase(BaseModel):
    Titulo: str
    Contenido: Optional[str] = None
    Imagen: Optional[str] = None
    FechaPublicacion: Optional[datetime] = None
    id_Usuario: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PublicacionCreate(PublicacionBase):
    pass

class PublicacionUpdate(PublicacionBase):
    pass

class PublicacionOut(PublicacionBase):
    Id: int
    NombreUsuario: str 

    class Config:
        orm_mode = True
