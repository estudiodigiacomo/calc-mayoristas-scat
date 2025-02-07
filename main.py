import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from google_sheets_module import conectar_google_sheets, leer_datos_hoja
from data_logic import obtener_proveedores, cargar_productos, actualizar_tipos, cargar_precio
from utils import obtener_cotizacion_dolar, actualizar_imagen_proveedor

# Conectar con Google Sheets
try:
    sheet = conectar_google_sheets("keys.json", "DB PROOVEDORES-SCATTONE")
except Exception as e:
    messagebox.showerror("Error", f"No se pudo conectar a Google Sheets. Detalle: {e}")
    sheet = None

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de Precios Mayorista de Pinturas Multimarca")
root.configure(bg="#f5f5f5")
root.geometry("1280x720")

# Variables de control
moneda_origen_var = tk.StringVar(value="ARS")
proveedor_var = tk.StringVar(value="")
producto_var = tk.StringVar(value="")
tipo_var = tk.StringVar(value="")
medida_var = tk.StringVar(value="")
color_var = tk.StringVar(value="")
cotizacion = tk.DoubleVar(value=1.0)
resultado_contado = tk.StringVar()
resultado_lista = tk.StringVar()

# Frames principales
frame_izquierda = ttk.Frame(root, padding=20)
frame_izquierda.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame_derecha = ttk.Frame(root, padding=20)
frame_derecha.grid(row=0, column=1, sticky=(tk.N, tk.E))

# Imagen del proveedor
imagen_proveedor_label = tk.Label(frame_derecha, text="Sin imagen", bg="#f5f5f5")
imagen_proveedor_label.grid(row=0, column=0, columnspan=2, pady=10)

# Dropdowns de selección
ttk.Label(frame_izquierda, text="Proveedor:", font=("Arial", 14)).grid(row=1, column=0, pady=5, sticky=tk.W)
proveedor_dropdown = ttk.Combobox(frame_izquierda, textvariable=proveedor_var, font=("Arial", 14), state="readonly", width=30)
proveedor_dropdown.grid(row=1, column=1, pady=5, sticky=tk.W)
proveedor_dropdown["values"] = obtener_proveedores()

ttk.Label(frame_izquierda, text="Producto:", font=("Arial", 14)).grid(row=2, column=0, pady=5, sticky=tk.W)
producto_dropdown = ttk.Combobox(frame_izquierda, textvariable=producto_var, font=("Arial", 14), state="readonly", width=30)
producto_dropdown.grid(row=2, column=1, pady=5, sticky=tk.W)

ttk.Label(frame_izquierda, text="Tipo:", font=("Arial", 14)).grid(row=3, column=0, pady=5, sticky=tk.W)
tipo_dropdown = ttk.Combobox(frame_izquierda, textvariable=tipo_var, font=("Arial", 14), state="readonly", width=30)
tipo_dropdown.grid(row=3, column=1, pady=5, sticky=tk.W)

ttk.Label(frame_izquierda, text="Medida o Cantidad:", font=("Arial", 14)).grid(row=4, column=0, pady=5, sticky=tk.W)
medida_dropdown = ttk.Combobox(frame_izquierda, textvariable=medida_var, font=("Arial", 14), state="readonly", width=30)
medida_dropdown.grid(row=4, column=1, pady=5, sticky=tk.W)

ttk.Label(frame_izquierda, text="Color:", font=("Arial", 14)).grid(row=5, column=0, pady=5, sticky=tk.W)
color_dropdown = ttk.Combobox(frame_izquierda, textvariable=color_var, font=("Arial", 14), state="readonly", width=30)
color_dropdown.grid(row=5, column=1, pady=5, sticky=tk.W)

# Vinculación de eventos
proveedor_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: cargar_productos(proveedor_var, sheet, frame_izquierda, imagen_proveedor_label, producto_dropdown, tipo_dropdown, medida_dropdown, color_dropdown, resultado_contado, resultado_lista, cotizacion_label, producto_var, tipo_var, medida_var, color_var, cotizacion),
)

producto_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: actualizar_tipos(proveedor_var, producto_var, tipo_dropdown, medida_dropdown, color_dropdown, tipo_var, medida_var, color_var),
)

tipo_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: cargar_precio(proveedor_var, producto_var, tipo_var, medida_var, color_var, resultado_contado, resultado_lista, cotizacion),
)

medida_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: cargar_precio(proveedor_var, producto_var, tipo_var, medida_var, color_var, resultado_contado, resultado_lista, cotizacion),
)

color_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: cargar_precio(proveedor_var, producto_var, tipo_var, medida_var, color_var, resultado_contado, resultado_lista, cotizacion),
)

# Botón para limpiar campos
def limpiar_campos():
    producto_dropdown["values"] = []
    producto_var.set("")
    tipo_dropdown["values"] = []
    tipo_var.set("")
    medida_dropdown["values"] = []
    medida_var.set("")
    color_dropdown["values"] = []
    color_var.set("")
    resultado_contado.set("")
    resultado_lista.set("")
    imagen_proveedor_label.config(image="", text="Sin imagen")

limpiar_button = ttk.Button(frame_derecha, text="Limpiar Campos", command=limpiar_campos)
limpiar_button.grid(row=5, column=0, columnspan=2, pady=20, sticky=tk.W)

# Resultados y precios
ttk.Label(frame_derecha, text="Precio Contado Efectivo:", font=("Arial", 14)).grid(row=1, column=0, pady=5, sticky=tk.W)
precio_contado_entry = ttk.Entry(frame_derecha, font=("Arial", 14), width=30, state="readonly", textvariable=resultado_contado)
precio_contado_entry.grid(row=1, column=1, pady=5, sticky=tk.W)

ttk.Label(frame_derecha, text="Precio Lista:", font=("Arial", 14)).grid(row=2, column=0, pady=5, sticky=tk.W)
precio_lista_entry = ttk.Entry(frame_derecha, font=("Arial", 14), width=30, state="readonly", textvariable=resultado_lista)
precio_lista_entry.grid(row=2, column=1, pady=5, sticky=tk.W)

# Obtener cotización inicial
cotizacion_label = ttk.Label(frame_derecha, text=f"Cotización actual: ${cotizacion.get():,.2f}", font=("Arial", 12, "italic"), foreground="gray")
cotizacion_label.grid(row=4, column=0, columnspan=2, pady=20, sticky=tk.W)
obtener_cotizacion_dolar(cotizacion, cotizacion_label)

# Iniciar aplicación
root.mainloop()
