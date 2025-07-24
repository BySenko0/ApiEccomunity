from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Likes_Comentarios(Base):
    __tablename__ = "likes_comentarios"

    Id = Column(Integer, primary_key=True, index=True)
    id_Comentario = Column(Integer, ForeignKey("comentarios.Id", ondelete="CASCADE"), nullable=False)
    id_Usuario = Column(Integer, ForeignKey("usuarios.Id", ondelete="CASCADE"), nullable=False)
    Fecha = Column(DateTime, server_default=func.now(), nullable=False)

    comentario = relationship("Comentario", back_populates="likes_comentarios")
    usuario = relationship("Usuario", back_populates="likes_comentarios")