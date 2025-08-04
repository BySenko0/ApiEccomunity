from pydantic import BaseModel
from datetime import datetime

class CentroTipoReciclajeBase(BaseModel):
    IdCentroReciclaje: int
    IdTipoReciclaje: int
    PrecioPorKg: float | None = None

class CentroTipoReciclajeCreate(CentroTipoReciclajeBase):
    pass

class CentroTipoReciclajeOut(CentroTipoReciclajeBase):
    Id: int
    fecha_creacion: datetime | None = None
    tipo_reciclaje_nombre: str

    class Config:
        orm_mode = True