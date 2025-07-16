from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Comentario(Base):
    __tablename__ = "comentarios"

    Id = Column(Integer, primary_key=True, index=True)
    Texto = Column(String(500), nullable=False)
    Fecha = Column(DateTime, server_default=func.now(), nullable=False)
    id_Publicacion = Column(Integer, ForeignKey("publicaciones.Id", ondelete="CASCADE"), nullable=False)
    id_Usuario = Column(Integer, ForeignKey("usuarios.Id", ondelete="CASCADE"), nullable=False)
    Likes = Column(Integer, default=0, nullable=False)

    publicacion = relationship("Publicacion", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")
