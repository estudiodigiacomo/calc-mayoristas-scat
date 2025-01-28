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

# Variables
moneda_origen_var = tk.StringVar(value="ARS")
proveedor_var = tk.StringVar(value="")
producto_var = tk.StringVar(value="")
tipo_var = tk.StringVar(value="")
cotizacion = tk.DoubleVar(value=1.0)
resultado_contado = tk.StringVar()
resultado_lista = tk.StringVar()

# Frames principales
frame_izquierda = ttk.Frame(root, padding=20)
frame_izquierda.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame_derecha = ttk.Frame(root, padding=20)
frame_derecha.grid(row=0, column=1, sticky=(tk.N, tk.E))

# Imagen del proveedor (en la derecha)
imagen_proveedor_label = tk.Label(frame_derecha, text="Sin imagen", bg="#f5f5f5")
imagen_proveedor_label.grid(row=0, column=0, columnspan=2, pady=10)

# Resultados (debajo de la imagen)
ttk.Label(frame_derecha, text="Precio Base:", font=("Arial", 14)).grid(row=1, column=0, pady=5, sticky=tk.W)
precio_base_entry = ttk.Entry(frame_derecha, font=("Arial", 14), width=30)
precio_base_entry.grid(row=1, column=1, pady=5, sticky=tk.W)

ttk.Label(frame_derecha, text="Precio Contado Efectivo:", font=("Arial", 14)).grid(row=2, column=0, pady=5, sticky=tk.W)
ttk.Label(frame_derecha, textvariable=resultado_contado, font=("Arial", 14)).grid(row=2, column=1, pady=5, sticky=tk.W)

ttk.Label(frame_derecha, text="Precio Lista:", font=("Arial", 14)).grid(row=3, column=0, pady=5, sticky=tk.W)
ttk.Label(frame_derecha, textvariable=resultado_lista, font=("Arial", 14)).grid(row=3, column=1, pady=5, sticky=tk.W)

# Cotización del dólar (al final en la derecha)
cotizacion_label = ttk.Label(
    frame_derecha,
    text=f"Cotización actual: ${cotizacion.get():,.2f}",
    font=("Arial", 12, "italic"),
    foreground="gray",
)
cotizacion_label.grid(row=4, column=0, columnspan=2, pady=20, sticky=tk.W)

# Secciones de la izquierda (selección de productos)
ttk.Label(frame_izquierda, text="Proveedor:", font=("Arial", 14)).grid(row=1, column=0, pady=5, sticky=tk.W)
proveedor_dropdown = ttk.Combobox(frame_izquierda, textvariable=proveedor_var, font=("Arial", 14), state="readonly", width=30)
proveedor_dropdown.grid(row=1, column=1, pady=5, sticky=tk.W)
proveedor_dropdown["values"] = obtener_proveedores()  # Carga los proveedores en el dropdown
proveedor_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: cargar_productos(
        proveedor_var,
        sheet,
        frame_izquierda,
        imagen_proveedor_label,
        producto_dropdown,
        tipo_dropdown,
        precio_base_entry,
        resultado_contado,
        resultado_lista,
        cotizacion_label,
        producto_var,
        tipo_var,
        cotizacion,
    ),
)

ttk.Label(frame_izquierda, text="Producto:", font=("Arial", 14)).grid(row=2, column=0, pady=5, sticky=tk.W)
producto_dropdown = ttk.Combobox(frame_izquierda, textvariable=producto_var, font=("Arial", 14), state="readonly", width=30)
producto_dropdown.grid(row=2, column=1, pady=5, sticky=tk.W)
producto_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: actualizar_tipos(proveedor_var, producto_var, frame_izquierda, tipo_dropdown),
)

ttk.Label(frame_izquierda, text="Tipo:", font=("Arial", 14)).grid(row=3, column=0, pady=5, sticky=tk.W)
tipo_dropdown = ttk.Combobox(frame_izquierda, textvariable=tipo_var, font=("Arial", 14), state="readonly", width=30)
tipo_dropdown.grid(row=3, column=1, pady=5, sticky=tk.W)
tipo_dropdown.bind(
    "<<ComboboxSelected>>",
    lambda e: cargar_precio(
        proveedor_var,
        producto_var,
        tipo_var,
        frame_izquierda,
        precio_base_entry,
        resultado_contado,
        resultado_lista,
        cotizacion_label,
        cotizacion,
    ),
)
widgets_dinamicos = []
def limpiar_campos():
    """
    Limpia todos los campos, widgets dinámicos, precios, y la imagen del proveedor.
    """
    print("Iniciando limpieza de campos...")  # Rastreo

    # Declarar widgets_dinamicos como global para usarlo correctamente
    global widgets_dinamicos

    # Limpiar valores de los dropdowns principales
    proveedor_var.set("")  # Reiniciar proveedor seleccionado
    print("Proveedor limpiado.")

    producto_dropdown["values"] = []
    producto_var.set("")  # Reiniciar producto seleccionado
    print("Producto limpiado.")

    tipo_dropdown["values"] = []
    tipo_var.set("")  # Reiniciar tipo seleccionado
    print("Tipo limpiado.")

    # Limpiar widgets dinámicos y sus valores
    for columna, widget in widgets_dinamicos:
        if isinstance(widget, ttk.Combobox):
            widget["values"] = []  # Limpiar las opciones del dropdown dinámico
            widget.set("")         # Reiniciar el valor seleccionado
        widget.destroy()           # Eliminar el widget de la interfaz
    widgets_dinamicos.clear()      # Limpiar la lista de widgets dinámicos
    print("Widgets dinámicos eliminados y valores limpiados.")

    # Limpiar entradas de precios y resultados
    precio_base_entry.delete(0, tk.END)
    resultado_contado.set("")
    resultado_lista.set("")
    print("Precios limpiados.")

    # Restablecer etiqueta de la imagen del proveedor
    imagen_proveedor_label.config(image="", text="Sin imagen")
    print("Imagen del proveedor reiniciada.")

    # Resetear la cotización del dólar en la interfaz (opcional)
    cotizacion_label.config(text=f"Cotización utilizada: ${cotizacion.get():,.2f}")
    print("Cotización reseteada.")

    print("Todos los campos, widgets dinámicos, precios e imagen han sido limpiados correctamente.")

limpiar_button = ttk.Button(frame_derecha, text="Limpiar Campos", command=limpiar_campos)
limpiar_button.grid(row=5, column=0, columnspan=2, pady=20, sticky=tk.W)

# Obtener cotización inicial
obtener_cotizacion_dolar(cotizacion, cotizacion_label)

# Iniciar aplicación
root.mainloop()
