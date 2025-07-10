from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# 🟢 Esquema para crear un tipo de reciclaje
class TipoReciclajeCreate(BaseModel):
    nombre: str
    peso_minimo: float
    peso_maximo: float
    pago_por_kg: float
    ganancia_por_kg: float
    fecha_creacion: date

# 🟡 Esquema para actualizar un tipo de reciclaje (todos los campos opcionales)
class TipoReciclajeUpdate(BaseModel):
    nombre: Optional[str] = None
    peso_minimo: Optional[float] = None
    peso_maximo: Optional[float] = None
    pago_por_kg: Optional[float] = None
    ganancia_por_kg: Optional[float] = None
    fecha_creacion: Optional[date] = None

# 🔵 Esquema para devolver datos al cliente
class TipoReciclajeOut(BaseModel):
    id: int = Field(alias="Id")
    nombre: str = Field(alias="Nombre")
    peso_minimo: float = Field(alias="PesoMinimo")
    peso_maximo: float = Field(alias="PesoMaximo")
    pago_por_kg: float = Field(alias="PagoPorKg")
    ganancia_por_kg: float = Field(alias="GananciaPorKg")
    fecha_creacion: date = Field(alias="FechaCreacion")

    class Config:
        from_attributes = True  # Permite leer atributos ORM (reemplaza orm_mode en Pydantic v2)
