from MonitorGUI import db

from hashlib import sha512

class LecturaError(Exception):
    def __init__(self, message):
        self.message = message

class Lectura(db.Model):
    __tablename__ = "lectura"
    # definimos el ID del usuario
    id = db.Column(db.Integer, primary_key=True)
    # bpm latido del corazon
    bpm = db.Column(db.Integer, nullable=False, unique=True)
    # señal analoga del modulo AD8232
    senialAnaloga = db.Column(db.Integer, nullable=False, unique=True)
    fechaHora = db.Column(db.Datetime, nullable=False)

    def __init__(self, bpm, senalAnaloga, fechaHora):
        self.bpm = bpm;
        self.senialAnaloga = senalAnaloga;
        self.fechaHora = fechaHora;