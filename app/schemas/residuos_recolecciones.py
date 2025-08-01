from pydantic import BaseModel
from datetime import datetime

class ResiduoRecoleccionBase(BaseModel):
    Cantidad: float
    IdRecoleccionUsuario: int
    IdTipoReciclajeCentro: int

class ResiduoRecoleccionCreate(ResiduoRecoleccionBase):
    pass

class ResiduoRecoleccionOut(ResiduoRecoleccionBase):
    Id: int

    class Config:
        orm_mode = True