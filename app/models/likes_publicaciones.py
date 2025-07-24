from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Likes_Publicaciones(Base):
    __tablename__ = "likes_publicaciones"

    Id = Column(Integer, primary_key=True, index=True)
    id_Publicacion = Column(Integer, ForeignKey("publicaciones.Id", ondelete="CASCADE"), nullable=False)
    id_Usuario = Column(Integer, ForeignKey("usuarios.Id", ondelete="CASCADE"), nullable=False)
    Fecha = Column(DateTime, server_default=func.now(), nullable=False)
    
    publicacion = relationship("Publicacion", back_populates="likes_publicaciones")
    usuario = relationship("Usuario", back_populates="likes_publicaciones")