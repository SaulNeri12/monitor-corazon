
"""
Monitor GUI - Usado para observar las lecturas almacenadas en la base de datos
"""


from app.sensor.ecg import obtener_lecturas_periodo

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

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

# Crear la ventana principal
root = tk.Tk()
root.title("Monitor de Corazon - Registro en Base de Datos")

# Crear un área de texto (Text widget)
text_area_label = tk.Label(root, text="Lecturas: ")
text_area_label.pack(padx=10, pady=5)

text_area = tk.Text(root, height=20, width=80)
text_area.pack(padx=10, pady=10)
text_area.config(state="disabled")

# Crear campos de fecha (solo Entry widgets para que el usuario ingrese las fechas manualmente)
fecha_inicio_label = tk.Label(root, text="Fecha de inicio (YYYY-MM-DD hh:mm):")
fecha_inicio_label.pack(padx=10, pady=5)

fecha_inicio = tk.Entry(root, width=20)
fecha_inicio.pack(padx=10, pady=5)

fecha_fin_label = tk.Label(root, text="Fecha de fin (YYYY-MM-DD hh:mm):")
fecha_fin_label.pack(padx=10, pady=5)

fecha_fin = tk.Entry(root, width=20)
fecha_fin.pack(padx=10, pady=5)

# Método para obtener las fechas con formato dd-MM-yyyy
def obtener_fechas() -> tuple:
    inicio_fecha = None
    fin_fecha = None
    
    if not (fecha_inicio.get() == None or len(fecha_inicio.get()) == 0):
        try:
            # Leer las fechas de los campos
            inicio = fecha_inicio.get()
            # Convertir al formato deseado
            inicio_formateado = datetime.strptime(inicio, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "El formato de la fecha de inicio es incorrecto.")
            
    if not (fecha_fin.get() == None or len(fecha_fin.get()) == 0):
        try:
            fin = fecha_fin.get()
            fin_formateado = datetime.strptime(fin, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "El formato de la fecha final es incorrecto.")
            
        if (fin <= inicio):
            messagebox.showerror("Error", "La fecha de fin no puede ser antes de la fecha de inicio.")
        
    return inicio_fecha, fin_fecha
        
def obtener_lecturas() -> None:
    # se obtienen los campos de fechas validados
    inicio, fin = obtener_fechas()
    # se obtiene la lista de lecuras en ese rango de fecha
    lecturas = obtener_lecturas_periodo(inicio, fin)
    # limpiamos el text area
    text_area.delete(1.0, tk.END)
    text_area.config(state="normal")
    for lectura in lecturas:
        #print(lectura)
        text_area.insert(tk.END, f"{lectura}\n")
        
    text_area.config(state="disabled")
    
    
# Botón para obtener las fechas
boton = tk.Button(root, text="Obtener Fechas", command=obtener_lecturas)
boton.pack(padx=10, pady=20)

def main():
    root.mainloop()

if __name__ == "__main__":
    main()