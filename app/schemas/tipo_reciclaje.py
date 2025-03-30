from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TipoReciclajeBase(BaseModel):
    Nombre: str = Field(..., min_length=1, max_length=100)
    PesoMinimo: Optional[float] = Field(default=None, ge=0)
    PesoMaximo: Optional[float] = Field(default=None, ge=0)
    PagoPorKg: Optional[float] = Field(default=None, ge=0)
    GananciaPorKg: Optional[float] = Field(default=None, ge=0)
    FechaCreacion: Optional[date] = None

class TipoReciclajeCreate(TipoReciclajeBase):
    pass

class TipoReciclajeUpdate(TipoReciclajeBase):
    pass

class TipoReciclajeOut(TipoReciclajeBase):
    Id: int

    class Config:
        from_attributes = True  # Para Pydantic v2 (usa orm_mode=True si usas v1)
