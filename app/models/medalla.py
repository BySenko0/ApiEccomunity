from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Medalla(Base):
    __tablename__ = "medallas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)          # ── añadimos descripción
    icono = Column(String(200), nullable=True)  

    usuarios = relationship("UsuarioMedalla", back_populates="medalla")


class UsuarioMedalla(Base):
    __tablename__ = "usuarios_medallas"

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.Id"))  # 👈 AJUSTADO aquí
    id_medalla = Column(Integer, ForeignKey("medallas.id"))
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)

    medalla = relationship("Medalla", back_populates="usuarios")
