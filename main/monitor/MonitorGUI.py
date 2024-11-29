
"""
Monitor en tiempo real del sensor AD8232
"""

from threading import Thread
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import time

from app.database import obtener_conexion_bd
from app.models import Lectura, LecturaException
from app.sensor.ecg import obtener_lectura_bpm
from app.config import Configuracion

"""
import datetime

sesion = obtener_conexion_bd()

lectura = Lectura(90, 80)
sesion.add(lectura)
sesion.commit()
sesion.close()
"""

# Crear la ventana principal
root = tk.Tk()
root.title("Monitor de Corazon")

# Crear un área de texto (Text widget)
text_area_label = tk.Label(root, text="Lecturas: ")
text_area_label.pack(padx=10, pady=5)

lecturas_text_area = tk.Text(root, height=20, width=80)
lecturas_text_area.pack(padx=10, pady=10)

# Crear campos de fecha (solo Entry widgets para que el usuario ingrese las fechas manualmente)
fecha_inicio_label = tk.Label(root, text="Fecha de inicio (YYYY-MM-DD):")
fecha_inicio_label.pack(padx=10, pady=5)

fecha_inicio = tk.Entry(root, width=20)
fecha_inicio.pack(padx=10, pady=5)

fecha_fin_label = tk.Label(root, text="Fecha de fin (YYYY-MM-DD):")
fecha_fin_label.pack(padx=10, pady=5)

fecha_fin = tk.Entry(root, width=20)
fecha_fin.pack(padx=10, pady=5)

# Botón para obtener las fechas y texto
boton = tk.Button(root, text="Obtener Fechas y Texto", command=None)
boton.pack(padx=10, pady=20)


# usado para detener el thread
recibir_lecturas_flg = True

def actualiza_panel_lecturas():
    while recibir_lecturas_flg:
        # se obtiene la lectura del modulo
        bpm = obtener_lectura_bpm()
        if (bpm != None): 
            # Obtiene la fecha y hora actual
            fecha_hora_actual = datetime.now()
            # Crear el string con f-string
            resultado = f"{fecha_hora_actual} -> BPM: {bpm}\n"
            # aqui deberia de guardar la lectura
            root.after(0, lecturas_text_area.insert, tk.END, resultado)
        else:
            print("### No se pudo obtener la lectura")
        # el hilo se detiene un tiempo antes de tomar otra lectura
        time.sleep(Configuracion.VELOCIDAD_LECTURA_SEGUNDOS)
        
hilo_actualiza_panel = Thread(target=actualiza_panel_lecturas, daemon=True)

def on_close():
    # Mostrar un mensaje de confirmación
    if messagebox.askyesno("Monitor RT - Salir", "¿Estás seguro de que deseas cerrar la ventana?"):
        root.destroy()  # Cerrar la ventana
        recibir_lecturas_flg = False
        print("### MonitorGUI.py -> Se cerro el frame")
    else:
        print("### MonitorGUI.py -> El cierre fue cancelado.")

# asignar el evento de cuando se quiere cerrar el frame
root.protocol("WM_DELETE_WINDOW", on_close)

def main():
    hilo_actualiza_panel.start()
    root.mainloop()

if __name__ == "__main__":
    main()
    