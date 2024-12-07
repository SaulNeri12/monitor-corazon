
"""
Monitor GUI - Usado para observar las lecturas almacenadas en la base de datos
"""

from app.sensor.ecg import obtener_lecturas_periodo

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

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
    try:
        # Validar fecha de inicio
        inicio = fecha_inicio.get()
        inicio_fecha = None
        if inicio:
            inicio_fecha = datetime.strptime(inicio, "%Y-%m-%d %H:%M")
        
        # Validar fecha de fin
        fin = fecha_fin.get()
        fin_fecha = None
        if fin:
            fin_fecha = datetime.strptime(fin, "%Y-%m-%d %H:%M")
        
        # Validar relación entre fechas (si ambas están presentes)
        if inicio_fecha and fin_fecha and fin_fecha <= inicio_fecha:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
        
        return inicio_fecha, fin_fecha
    
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return None, None
       
        
def obtener_lecturas() -> None:
    # se obtienen los campos de fechas validados
    inicio, fin = obtener_fechas()
    # se obtiene la lista de lecuras en ese rango de fecha
    lecturas = obtener_lecturas_periodo(inicio, fin)
    # limpiamos el text area
    text_area.config(state="normal")
    text_area.delete(1.0, tk.END)
    for lectura in lecturas:
        #print(lectura)
        text_area.insert(tk.END, f"{lectura}\n")
        
    text_area.config(state="disabled")
    
    
# Botón para obtener las fechas
boton = tk.Button(root, text="Obtener Lecturas", command=obtener_lecturas)
boton.pack(padx=10, pady=20)

def main():
    root.mainloop()

if __name__ == "__main__":
    main()