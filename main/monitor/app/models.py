from sqlalchemy import Column, Integer, DateTime
from app.database import engine
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()

class LecturaException(Exception):
    def __init__(self, message):
        self.message = message

class Lectura(Base):
    """Representa una lectura del ritmo cardiaco"""
    __tablename__ = "lectura"
    # id de la lectura en la base de datos
    id = Column(Integer, primary_key=True)
    # bpm latido del corazon
    bpm = Column(Integer, nullable=False)
    # señal analoga del modulo AD8232
    senial_analoga = Column(Integer, nullable=False)
    # fecha y hora exacta en que se capturo la lectura
    fecha_hora = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, bpm, senal_analoga):
        self.bpm = bpm;
        self.senial_analoga = senal_analoga;
        
# crea todos los modelos que se registran aqui
Base.metadata.create_all(engine)