import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import os

def obtener_cotizacion_dolar():
    try:
        api_url = "https://dolarapi.com/v1/dolares/oficial"
        headers = {"Content-Type": "application/json"}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(data['venta'])
        else:
            raise ValueError("Error al obtener los datos de la API.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la cotización del dólar. No se puede continuar.")
        return False
    
obtener_cotizacion_dolar()


############################
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import io
from google_sheets import conectar_google_sheets, leer_datos_hoja

# Conectar con Google Sheets
try:
    sheet = conectar_google_sheets('keys.json', 'DB PROOVEDORES-SCATTONE')
except Exception as e:
    messagebox.showerror("Error", f"No se pudo conectar a Google Sheets. Detalle: {e}")
    sheet = None

# Diccionario con los datos de los proveedores y sus multiplicadores
proveedores = {
    "Bambin": {"contado": 1.94, "lista": 2.19, "imagen": "https://storage.googleapis.com/scatone_proovedores/bambin.webp"},
    "COPSA": {"contado": 1.74, "lista": 2, "imagen": "https://storage.googleapis.com/scatone_proovedores/copsa.png"},
    "El Mastin": {"contado": 1.880, "lista": 2.14, "imagen": "https://storage.googleapis.com/scatone_proovedores/el-mastin.jpg"},
    "Grizzly": {"contado": 1.94, "lista": 2.46, "imagen": "https://storage.googleapis.com/scatone_proovedores/grizzly.png"},
    "Lomel": {"contado": 1.94, "lista": 2.23, "imagen": "https://storage.googleapis.com/scatone_proovedores/lomel.jpg"},
    "Pintureria Rex": {"contado": 1.84, "lista": 2.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/rex.png"},
    "Sistinar": {"contado": 1.62, "lista": 2.22, "imagen": "https://storage.googleapis.com/scatone_proovedores/sistinar.jpg"},
    "Bell Color": {"contado": 1789, "lista": 2260, "imagen": "https://storage.googleapis.com/scatone_proovedores/bellcolor.png"},
    "Expocolor": {"contado": 2022.40, "lista":  2618.16, "imagen": "https://storage.googleapis.com/scatone_proovedores/expocolor.png"},
    "Macavi": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg"},
    "Sherwin Williams": {"contado": 2027.26, "lista": 2438.55, "imagen": "https://storage.googleapis.com/scatone_proovedores/sherwin-williams.jpg"},
}

# Variables para la carga dinámica
productos = {}
tipos = {}
cantidades = {}

# Función para cargar productos dinámicamente desde Google Sheets
def cargar_productos(event):
    proveedor_seleccionado = proveedor_var.get()
    if not proveedor_seleccionado:
        return

    # Verificar conexión con Google Sheets
    if not sheet:
        messagebox.showerror("Error", "No se pudo conectar a Google Sheets. Verifique la configuración.")
        return

    try:
        # Leer datos de la hoja del proveedor seleccionado
        datos = leer_datos_hoja(sheet, proveedor_seleccionado)
        productos.clear()
        tipos.clear()
        cantidades.clear()

        for fila in datos:
            producto = fila["Producto"]
            tipo = fila["Tipo"]
            cantidad = fila["Medida o Cantidad"]

            if producto not in productos:
                productos[producto] = {}
            if tipo not in productos[producto]:
                productos[producto][tipo] = []
            productos[producto][tipo].append(cantidad)

        # Actualizar dropdown de productos
        producto_dropdown["values"] = list(productos.keys())
        producto_var.set("")
        tipo_dropdown["values"] = []
        medida_dropdown["values"] = []
        precio_base_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos. Detalle: {e}")

def actualizar_tipos(event):
    producto_seleccionado = producto_var.get()
    if not producto_seleccionado or producto_seleccionado not in productos:
        tipo_dropdown["values"] = []
        tipo_var.set("")
        return

    # Actualizar dropdown de tipos
    tipo_dropdown["values"] = list(productos[producto_seleccionado].keys())
    tipo_var.set("")
    medida_dropdown["values"] = []
    precio_base_entry.delete(0, tk.END)

def actualizar_cantidades(event):
    producto_seleccionado = producto_var.get()
    tipo_seleccionado = tipo_var.get()
    if not producto_seleccionado or not tipo_seleccionado:
        medida_dropdown["values"] = []
        medida_var.set("")
        return

    # Actualizar dropdown de medidas o cantidades
    medida_dropdown["values"] = productos[producto_seleccionado][tipo_seleccionado]
    medida_var.set("")
    precio_base_entry.delete(0, tk.END)

# Función para cargar precio automáticamente según la selección
def cargar_precio(event):
    proveedor_seleccionado = proveedor_var.get()
    producto_seleccionado = producto_var.get()
    tipo_seleccionado = tipo_var.get()
    medida_seleccionada = medida_var.get()

    if not (proveedor_seleccionado and producto_seleccionado and tipo_seleccionado and medida_seleccionada):
        return

    try:
        # Leer datos de la hoja y encontrar el precio
        datos = leer_datos_hoja(sheet, proveedor_seleccionado)
        for fila in datos:
            if (fila["Producto"] == producto_seleccionado and
                    fila["Tipo"] == tipo_seleccionado and
                    fila["Medida o Cantidad"] == medida_seleccionada):
                precio_base_entry.delete(0, tk.END)
                precio_base_entry.insert(0, fila["Precio"] if moneda_origen_var.get() == "ARS" else fila["Precio USD"])
                break
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el precio. Detalle: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de Precios Mayorista de Pinturas Multimarca")
root.configure(bg="#f5f5f5")
root.geometry("1024x768")

# Variables de Tkinter
moneda_origen_var = tk.StringVar(value="ARS")
proveedor_var = tk.StringVar(value="Proveedor")
producto_var = tk.StringVar(value="")
tipo_var = tk.StringVar(value="")
medida_var = tk.StringVar(value="")
resultado_contado = tk.StringVar()
resultado_lista = tk.StringVar()
cotizacion = tk.DoubleVar(value=1.0)
multiplicador_contado = tk.DoubleVar()
multiplicador_lista = tk.DoubleVar()

# Dropdowns dinámicos añadidos al Frame
ttk.Label(root, text="Proveedor:").grid(row=0, column=0)
proveedor_dropdown = ttk.Combobox(root, textvariable=proveedor_var, values=list(proveedores.keys()), state="readonly")
proveedor_dropdown.grid(row=0, column=1)
proveedor_dropdown.bind("<<ComboboxSelected>>", cargar_productos)

ttk.Label(root, text="Producto:").grid(row=1, column=0)
producto_dropdown = ttk.Combobox(root, textvariable=producto_var, state="readonly")
producto_dropdown.grid(row=1, column=1)
producto_dropdown.bind("<<ComboboxSelected>>", actualizar_tipos)

ttk.Label(root, text="Tipo:").grid(row=2, column=0)
tipo_dropdown = ttk.Combobox(root, textvariable=tipo_var, state="readonly")
tipo_dropdown.grid(row=2, column=1)
tipo_dropdown.bind("<<ComboboxSelected>>", actualizar_cantidades)

ttk.Label(root, text="Medida o Cantidad:").grid(row=3, column=0)
medida_dropdown = ttk.Combobox(root, textvariable=medida_var, state="readonly")
medida_dropdown.grid(row=3, column=1)
medida_dropdown.bind("<<ComboboxSelected>>", cargar_precio)

# Entrada para el precio base
ttk.Label(root, text="Precio Base:").grid(row=4, column=0)
precio_base_entry = ttk.Entry(root)
precio_base_entry.grid(row=4, column=1)

# Iniciar la aplicación
root.mainloop()
