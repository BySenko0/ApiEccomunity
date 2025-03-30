from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class RecoleccionUsuario(Base):
    __tablename__ = "recoleccionesusuarios"

    Id = Column(Integer, primary_key=True, index=True)
    Tipo = Column(String(100), nullable=False)  # Cambiado a String si es un nombre de tipo
    Dia = Column(Date, nullable=False)          # Recomendado usar Date en lugar de String
    Hora = Column(Time, nullable=False)
    Cantidad = Column(Float, nullable=False)    # Mejor tipo para representar peso
    Status = Column(String(50), nullable=False)

    id_PuntoRecoleccion = Column(Integer, ForeignKey("puntosrecoleccion.Id", ondelete="CASCADE"), nullable=False)
    id_Usuario = Column(Integer, ForeignKey("usuarios.Id", ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", back_populates="recolecciones")
    punto_recoleccion = relationship("PuntoRecoleccion", back_populates="recolecciones_usuarios")
