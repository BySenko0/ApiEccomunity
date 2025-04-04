from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    Nombre: str
    Correo: EmailStr
    Ubicacion: Optional[str]
    Rol: Optional[str] = "usuario"
    Estado: Optional[str]
    Cooldown: Optional[str]
    url_perfil: Optional[str]

class UsuarioCreate(UsuarioBase):
    contrasena: str


class UsuarioUpdate(BaseModel):
    Nombre: Optional[str]
    Ubicacion: Optional[str]
    Rol: Optional[str]
    Estado: Optional[str]
    Cooldown: Optional[str]
    url_perfil: Optional[str]

class UsuarioOut(UsuarioBase):
    Id: int
    FechaCreacion: Optional[datetime]

    class Config:
        orm_mode = True
