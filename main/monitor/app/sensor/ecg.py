from requests.exceptions import InvalidURL
import requests

from app.config import Configuracion

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
        