from pydantic import BaseModel
from datetime import datetime

class LikeComentarioBase(BaseModel):
    id_Comentario: int
    id_Usuario: int

class LikeComentarioCreate(LikeComentarioBase):
    pass

class LikeComentarioOut(LikeComentarioBase):
    Id: int
    Fecha: datetime

    class Config:
        orm_mode = True