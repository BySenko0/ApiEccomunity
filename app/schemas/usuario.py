from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic import Field


class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    ubicacion: Optional[str] = None
    rol: Optional[str] = "usuario"
    estado: Optional[str] = None
    cooldown: Optional[str] = None
    url_perfil: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None
    cooldown: Optional[str] = None
    url_perfil: Optional[str] = None

class UsuarioOut(BaseModel):
    id: int = Field(alias="Id")
    nombre: str = Field(alias="Nombre")
    correo: EmailStr = Field(alias="Correo")
    ubicacion: Optional[str] = Field(alias="Ubicacion", default=None)
    rol: str = Field(alias="Rol")
    estado: Optional[str] = Field(alias="Estado", default=None)
    cooldown: Optional[str] = Field(alias="Cooldown", default=None)
    url_perfil: Optional[str] = Field(alias="url_perfil", default=None)
    fecha_creacion: Optional[datetime] = Field(alias="FechaCreacion", default=None)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
