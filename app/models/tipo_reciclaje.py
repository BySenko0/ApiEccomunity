# models/tipo_reciclaje.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TipoReciclaje(Base):
    __tablename__ = "tiposreciclaje"

    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False, unique=True)
    PesoMinimo = Column(Float, nullable=True)
    PesoMaximo = Column(Float, nullable=True)
    PagoPorKg = Column(Float, nullable=True)
    GananciaPorKg = Column(Float, nullable=True)
    FechaCreacion = Column(Date, nullable=True)  

    centros_tipos_reciclaje = relationship("CentroTipoReciclaje", back_populates="tipo_reciclaje", cascade="all, delete-orphan")