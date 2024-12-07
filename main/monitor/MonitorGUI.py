
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
from app.config import Configuracion, inicializar_configuracion

import sys

if len(sys.argv) < 2:
    print("[=!=] Porfavor proporciona la IP asignada por el router a el ESP32")
    sys.exit(1)
else:
    print(sys.argv[1])
    inicializar_configuracion(sys.argv[1])

# usado para abrir la ventana con la pagina de muestra 
# en tiempo real del sensor
import os
import webbrowser

# Obtener la ruta del archivo .html que muestra
# la grafica en tiempo real
ruta_actual = os.getcwd()
carpeta_data = os.path.dirname(ruta_actual)
pagina_sensor = os.path.join(carpeta_data, "data", "pagina.html")
webbrowser.open(pagina_sensor)

# usado para interactuar con la base de datos...
sesionBD = obtener_conexion_bd()

# Crear la ventana principal
root = tk.Tk()
root.title("Monitor de Corazon - Tiempo Real")

# Crear un área de texto (Text widget)
text_area_label = tk.Label(root, text="Lecturas: ")
text_area_label.pack(padx=10, pady=5)

lecturas_text_area = tk.Text(root, height=20, width=80)
lecturas_text_area.pack(padx=10, pady=10)

def limpiar_log_lecturas():
    lecturas_text_area.delete(1.0, tk.END)

# Botón para obtener las fechas y texto
boton_limpiar = tk.Button(root, text="limpiar Resultados", command=limpiar_log_lecturas)
boton_limpiar.pack(padx=10, pady=20)

# usado para detener el thread
recibir_lecturas_flg = True

def actualiza_panel_lecturas():
    global sesionBD
    
    lecturas = list()
    
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
            # anado la lectura a la lista
            if (len(lecturas) != Configuracion.PRECISION_LECTURAS):
                lecturas.append(bpm)
        else:
            print("### No se pudo obtener la lectura")
        
        # se verifica si la lista de lecturas esta llena para
        # sacar la media de precision y agregar la lectura en la base de datos
        if (len(lecturas) == Configuracion.PRECISION_LECTURAS):
            # se calcula la media
            media_bpm = int(sum(lecturas) / len(lecturas))
            # se crea la lectura
            lectura = Lectura(bpm=media_bpm, senal_analoga=media_bpm)
            # se anade al stack de modelos a agregar
            sesionBD.add(lectura)
            # se guardan los cambios
            sesionBD.commit()
            # se limpia la lista para volver a llenarse
            lecturas.clear()
            print("### MonitorGUI.py -> SE GUARDO LA LECTURA DE LA MEDIA DE BPM: {}".format(media_bpm))
            
        # el hilo se detiene un tiempo antes de tomar otra lectura
        time.sleep(Configuracion.VELOCIDAD_LECTURA_SEGUNDOS)


# ejecuta de manera paralela consultas al modulo AD8232 a traves del servidor
# del ESP32
hilo_actualiza_panel = Thread(target=actualiza_panel_lecturas, daemon=True)

def on_close():
    """Operacion que sucede cuando se cierra el frame"""
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
    # se ejecuta la operacion paralela de consultas al modulo AD8232
    hilo_actualiza_panel.start()
    # se ejecuta la Interfaz Grafica
    root.mainloop()
    # se cierra la conexion con la base de datos
    sesionBD.close()

if __name__ == "__main__":
    main()
    