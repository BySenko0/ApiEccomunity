from pydantic import BaseModel
from datetime import datetime

class UsuarioMedallaBase(BaseModel):
    id_usuario: int
    id_medalla: int

class UsuarioMedallaCreate(UsuarioMedallaBase):
    pass

class UsuarioMedallaOut(UsuarioMedallaBase):
    fecha_asignacion: datetime

    class Config:
        orm_mode = True
