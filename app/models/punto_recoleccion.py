from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.orm import relationship
from app.database import Base

class PuntoRecoleccion(Base):
    __tablename__ = "puntosrecoleccion"

    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255), nullable=False)
    Ubicacion = Column(String(255), nullable=True)
    Latitud = Column(Double, nullable=True)
    Longitud = Column(Double, nullable=True)
    FechaCreacion = Column(Date, nullable=True)

    recolecciones_usuarios = relationship("RecoleccionUsuario", back_populates="punto_recoleccion", cascade="all, delete-orphan")
    centros_tipos_reciclaje = relationship("CentroTipoReciclaje", back_populates="punto_recoleccion", cascade="all, delete-orphan")
