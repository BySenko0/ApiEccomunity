from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic import Field

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime
from pydantic import Field


class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    ubicacion: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None
    cooldown: Optional[str] = None
    url_perfil: Optional[str] = None
    imagen_perfil: Optional[str] = None
    imagen_fondo: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None
    cooldown: Optional[str] = None
    url_perfil: Optional[str] = None
    imagen_perfil: Optional[str] = None
    imagen_fondo: Optional[str] = None

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
    imagen_perfil: Optional[str] = Field(alias="Imagen_perfil", default='default.png')
    imagen_fondo: Optional[str] = Field(alias="Imagen_fondo", default=None)
    ImagenPerfilUrl: Optional[HttpUrl] = None  # Nueva URL de imagen de perfil
    ImagenFondoUrl: Optional[HttpUrl] = None   # Nueva URL de imagen de fondo

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            'HttpUrl': lambda v: str(v) if v else None,
            'datetime': lambda v: v.isoformat()
        }
