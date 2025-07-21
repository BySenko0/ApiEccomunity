from pydantic import BaseModel
from datetime import datetime as date

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

    class Config:
        orm_mode = True