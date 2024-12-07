"""
Contiene las variables de configuracion de la aplicacion
"""

import socket
import sys

class Configuracion():
    IP_CONEXION_ESP32 = ""
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:19040042@localhost/monitor_corazon"
    MONITOR_CORAZON_URL = "http://192.168.0.139"
    MONITOR_CORAZON_SENSOR_BPM_URL = "http://192.168.0.139/bpm"
    MONITOR_CORAZON_SENSOR_ECG_URL = "http://192.168.0.139/ecg"
    # datos por defecto
    VELOCIDAD_LECTURA_SEGUNDOS = 2 # dos segundos cada lectura
    PRECISION_LECTURAS = 10 # media de un arreglo de 10 lecturas


def inicializar_configuracion(ip: str) -> None:
    try:
        ip_valida = socket.inet_aton(ip)
        if not ip_valida:
            sys.exit(1)
    except OSError:
        print("[!] Error: La IP dada no es valida")
        sys.exit(1)
        
    Configuracion.IP_CONEXION_ESP32 = ip
    Configuracion.MONITOR_CORAZON_URL = f"http://{ip}"
    Configuracion.MONITOR_CORAZON_SENSOR_BPM_URL = f"{Configuracion.MONITOR_CORAZON_URL}/bpm"
    Configuracion.MONITOR_CORAZON_SENSOR_ECG_URL = f"{Configuracion.MONITOR_CORAZON_URL}/ecg"
