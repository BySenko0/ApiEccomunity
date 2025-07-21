from pydantic import BaseModel
from datetime import datetime

class LikePublicacionBase(BaseModel):
    id_Publicacion: int
    id_Usuario: int

class LikePublicacionCreate(LikePublicacionBase):
    pass

class LikePublicacionOut(LikePublicacionBase):
    Id: int
    Fecha: datetime

    class Config:
        orm_mode = True