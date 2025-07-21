from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255), nullable=False)
    Correo = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    Ubicacion = Column(String(255), nullable=True)
    Rol = Column(Enum("usuario", "admin", name="rol_enum"), default="usuario", nullable=False)
    Estado = Column(String(50), nullable=True)
    Cooldown = Column(String(50), nullable=True)
    url_perfil = Column(String(255), nullable=True)
    FechaCreacion = Column(DateTime, server_default=func.now(), nullable=False)

    publicaciones = relationship("Publicacion", back_populates="autor", cascade="all, delete")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete")
    recolecciones = relationship("RecoleccionUsuario", back_populates="usuario", cascade="all, delete")
    
    # ✅ Relación correcta hacia tabla intermedia
    usuario_medallas = relationship("UsuarioMedalla", backref="usuario", cascade="all, delete")

    likes_publicaciones = relationship("Likes_Publicaciones", back_populates="usuario", cascade="all, delete")
    likes_comentarios = relationship("Likes_Comentarios", back_populates="usuario", cascade="all, delete")