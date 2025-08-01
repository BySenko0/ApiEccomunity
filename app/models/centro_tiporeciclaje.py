from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func, Float
from sqlalchemy.orm import relationship
from app.database import Base

class CentroTipoReciclaje(Base):
    __tablename__ = "centros_tipos_reciclaje"

    Id = Column(Integer, primary_key=True, index=True)
    IdCentroReciclaje = Column(Integer, ForeignKey("puntosrecoleccion.Id", ondelete="CASCADE"), nullable=False) 
    IdTipoReciclaje = Column(Integer, ForeignKey("tiposreciclaje.Id", ondelete="CASCADE"), nullable=False) 
    PrecioPorKg = Column(Float, nullable=True)

    punto_recoleccion = relationship("PuntoRecoleccion", back_populates="centros_tipos_reciclaje")
    tipo_reciclaje = relationship("TipoReciclaje", back_populates="centros_tipos_reciclaje")
    residuos_recolecciones = relationship("ResiduosRecolecciones", back_populates="centro_tipo_reciclaje", cascade="all, delete-orphan")