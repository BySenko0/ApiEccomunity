from pydantic import BaseModel
from datetime import date

class ComentarioBase(BaseModel):
    Texto: str
    Fecha: date
    id_Publicacion: int
    id_Usuario: int
    Likes:int

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioUpdate(ComentarioBase):
    pass

class ComentarioOut(ComentarioBase):
    Id: int

    class Config:
        orm_mode = True
