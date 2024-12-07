"""
Contiene las variables de configuracion de la aplicacion
"""

class Configuracion():
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:19040042@localhost/monitor_corazon"
    MONITOR_CORAZON_URL = "http://192.168.0.139/bpm"
    MONITOR_CORAZON_SENSOR_BPM_URL = "http://192.168.0.139/bpm"
    VELOCIDAD_LECTURA_SEGUNDOS = 2 # dos segundos cada lectura
    PRECISION_LECTURAS = 10 # media de un arreglo de 10 lecturas