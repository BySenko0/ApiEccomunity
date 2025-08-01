from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func, Float
from sqlalchemy.orm import relationship
from app.database import Base

class ResiduosRecolecciones(Base):
    __tablename__ = "residuos_recolecciones"

    Id = Column(Integer, primary_key=True, index=True)
    IdRecoleccionUsuario = Column(Integer, ForeignKey("recoleccionesusuarios.Id", ondelete="CASCADE"), nullable=False)
    IdTipoReciclajeCentro = Column(Integer, ForeignKey("centros_tipos_reciclaje.Id", ondelete="CASCADE"), nullable=False)
    Cantidad = Column(Float, nullable=False) 

    recoleccion_usuario = relationship("RecoleccionUsuario", back_populates="residuos_recolecciones")
    centro_tipo_reciclaje = relationship("CentroTipoReciclaje", back_populates="residuos_recolecciones")