from pydantic import BaseModel
from typing import Optional
from datetime import time, date

class RecoleccionBase(BaseModel):
    Tipo: int
    Dia: date
    Hora: time
    Cantidad: float
    Status: str
    id_PuntoRecoleccion: int
    id_Usuario: int

class RecoleccionCreate(RecoleccionBase):
    pass

class RecoleccionUpdate(RecoleccionBase):
    pass

class StatusUpdate(BaseModel):
    nuevo_status: str

class RecoleccionOut(RecoleccionBase):
    Id: int
    PuntoRecoleccion: str
    DireccionPunto: str
    UsuarioNombre: str

    class Config:
        orm_mode = True
