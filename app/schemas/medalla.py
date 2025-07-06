from pydantic import BaseModel

class MedallaBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    icono: str | None = None

class MedallaCreate(MedallaBase):
    pass

class MedallaOut(MedallaBase):
    id: int

    class Config:
        orm_mode = True
