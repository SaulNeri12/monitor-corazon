
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Configuracion

# Crear el motor de conexión con la base de datos
engine = create_engine(Configuracion.SQLALCHEMY_DATABASE_URI, echo=True)

# Crear una sesión para interactuar con la base de datos (Sesion unica)
Session = sessionmaker(bind=engine)

def obtener_conexion_bd():
    """Devuelve una sesion para interactuar con la base de datos"""
    return Session()