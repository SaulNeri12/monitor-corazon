import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Monitor de Corazon")

# Crear un área de texto (Text widget)
text_area_label = tk.Label(root, text="Lecturas: ")
text_area_label.pack(padx=10, pady=5)

text_area = tk.Text(root, height=10, width=40)
text_area.pack(padx=10, pady=10)

# Crear campos de fecha (solo Entry widgets para que el usuario ingrese las fechas manualmente)
fecha_inicio_label = tk.Label(root, text="Fecha de inicio (YYYY-MM-DD):")
fecha_inicio_label.pack(padx=10, pady=5)

fecha_inicio = tk.Entry(root, width=20)
fecha_inicio.pack(padx=10, pady=5)

fecha_fin_label = tk.Label(root, text="Fecha de fin (YYYY-MM-DD):")
fecha_fin_label.pack(padx=10, pady=5)

fecha_fin = tk.Entry(root, width=20)
fecha_fin.pack(padx=10, pady=5)

# Función que se ejecuta al presionar el botón
def obtener_fecha():
    inicio = fecha_inicio.get()
    fin = fecha_fin.get()
    print(f"Fecha de inicio: {inicio}")
    print(f"Fecha de fin: {fin}")
    print("Texto ingresado en el área de texto:")
    print(text_area.get("1.0", tk.END))

# Botón para obtener las fechas y texto
boton = tk.Button(root, text="Obtener Fechas y Texto", command=obtener_fecha)
boton.pack(padx=10, pady=20)

# Ejecutar la ventana principal
root.mainloop()

