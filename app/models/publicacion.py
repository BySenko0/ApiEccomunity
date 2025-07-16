from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Publicacion(Base):
    __tablename__ = "publicaciones"

    Id = Column(Integer, primary_key=True, index=True)
    Titulo = Column(String(255), nullable=False)
    Contenido = Column(String(1000), nullable=True)
    Imagen = Column(String(255), nullable=True)
    FechaPublicacion = Column(DateTime, server_default=func.now(), nullable=False)
    id_Usuario = Column(Integer, ForeignKey("usuarios.Id", ondelete="CASCADE"), nullable=False)
    Likes = Column(Integer, default=0, nullable=False)

    autor = relationship("Usuario", back_populates="publicaciones")
    comentarios = relationship("Comentario", back_populates="publicacion", cascade="all, delete")
