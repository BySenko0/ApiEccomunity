from pydantic import BaseModel
from datetime import datetime as date
from typing import Optional

class PublicacionBase(BaseModel):
    Titulo: str
    Contenido: Optional[str]
    Imagen: Optional[str]
    FechaPublicacion: date
    id_Usuario: int

class PublicacionCreate(PublicacionBase):
    pass

class PublicacionUpdate(PublicacionBase):
    pass

class PublicacionOut(PublicacionBase):
    Id: int
    NombreUsuario: str 

    class Config:
        orm_mode = True
