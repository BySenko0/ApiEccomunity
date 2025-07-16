from pydantic import BaseModel
from datetime import date
from typing import Optional

class PublicacionBase(BaseModel):
    Titulo: str
    Contenido: Optional[str]
    Imagen: Optional[str]
    FechaPublicacion: date
    id_Usuario: int
    Likes: int

class PublicacionCreate(PublicacionBase):
    pass

class PublicacionUpdate(PublicacionBase):
    pass

class PublicacionOut(PublicacionBase):
    Id: int

    class Config:
        orm_mode = True
