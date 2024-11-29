"""
Contiene las variables de configuracion de la aplicacion
"""

class Configuracion():
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:19040042@localhost/monitor_corazon"
    MONITOR_CORAZON_URL = "http:"
    MONITOR_CORAZON_SENSOR_BOM_URL = "http://192.168.0.103/bpm"
    VELOCIDAD_LECTURA_SEGUNDOS = 2 # dos segundos cada lectura