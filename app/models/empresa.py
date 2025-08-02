from sqlalchemy import Column, DateTime, Integer, String, Date, func
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresa"

    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255), nullable=False, unique=True)
    Ubicacion = Column(String(255), nullable=True)
    Correo = Column(String(255), nullable=True)
    Telefono = Column(String(20), nullable=True)
    FechaCreacion = Column(DateTime, server_default=func.now(), nullable=True)

    tipos_reciclaje = relationship("EmpresaTipoReciclaje", back_populates="empresa", cascade="all, delete")
    recolecciones_empresa = relationship("RecoleccionEmpresa", back_populates="empresa", cascade="all, delete")
