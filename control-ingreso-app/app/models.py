from sqlalchemy import Column,Integer,String,Boolean

from .database import Base


class Empleado(Base):
    __tablename__ = 'empleados'
    id = Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String)
    apellidos = Column(String)
    rut = Column(String)
    email = Column(String)
    cargo = Column(String)
    empresa = Column(String)
    fecha = Column(String)
    hora = Column(String)
    registrado = Column(Boolean,default=False)