
from app.config import Configuracion
from app.database import obtener_conexion_bd
from app.models import Lectura

from datetime import datetime
from requests.exceptions import InvalidURL
import requests

from sqlalchemy import and_

def parse_bpm_str(bpm_str: str) -> int:
    """Convierte la lectura del BPM a entero. Caso contrario devuelve None cuando ocurre un error."""
    try:
        numero = int(bpm_str)
        return numero
    except ValueError:
        print("### sensor.py -> no se pudo obtener el BPM del servidor (HTTP: {})")
        return None

def obtener_lectura_bpm() -> str:
    """Obtiene la lectura BPM del sensor AD8232 en el servidor del monitor"""
    try:
        response = requests.get(Configuracion.MONITOR_CORAZON_SENSOR_BPM_URL)
        status = response.status_code
        return parse_bpm_str(response.text) if (status == 200) else None
    except InvalidURL:
        print("### ecg.py -> La URL del sensor tiene un formato incorrecto")
        return None

def obtener_lecturas_periodo(inicio: datetime, fin: datetime):
    """Busca lecturas de BPM almacenadas en la base de datos en un periodo de tiempo"""
    # obtenemos la conexion a la base de datos
    bd = obtener_conexion_bd()
    # Si ambas fechas están presentes, aplica el filtro
    
    resultados = list()
    if inicio and fin:
        resultados = bd.query(Lectura).filter(
            and_(Lectura.fecha_hora >= inicio, Lectura.fecha_hora <= fin)
        ).all()
    else:
        # Si alguna fecha es None, ajusta el filtro
        if inicio:
            # Si solo la fecha de inicio es proporcionada
            resultados = bd.query(Lectura).filter(Lectura.fecha_hora >= inicio).all()
        elif fin:
            # Si solo la fecha de fin es proporcionada
            resultados = bd.query(Lectura).filter(Lectura.fecha_hora <= fin).all()
        else:
            # Si no hay fechas proporcionadas
            resultados = bd.query(Lectura).all()
    
    return resultados