#data_logic.py
from tkinter import ttk, messagebox
import tkinter as tk
from utils import actualizar_imagen_proveedor
from google_sheets_module import leer_datos_hoja

proveedores = {
    "Bambin": {"contado": 1.94, "lista": 2.19, "imagen": "https://storage.googleapis.com/scatone_proovedores/bambin.webp", "moneda": "ARS"},
    "COPSA": {"contado": 1.74, "lista": 2, "imagen": "https://storage.googleapis.com/scatone_proovedores/copsa.png", "moneda": "ARS"},
    "El Mastin": {"contado": 1.880, "lista": 2.14, "imagen": "https://storage.googleapis.com/scatone_proovedores/el-mastin.jpg", "moneda": "ARS"},
    "Grizzly": {"contado": 1.94, "lista": 2.46, "imagen": "https://storage.googleapis.com/scatone_proovedores/grizzly.png", "moneda": "ARS"},
    "Lomel": {"contado": 1.94, "lista": 2.23, "imagen": "https://storage.googleapis.com/scatone_proovedores/lomel.jpg", "moneda": "ARS"},
    "Pintureria Rex": {"contado": 1.84, "lista": 2.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/rex.png", "moneda": "ARS"},
    "Sistinar": {"contado": 1.62, "lista": 2.22, "imagen": "https://storage.googleapis.com/scatone_proovedores/sistinar.jpg", "moneda": "ARS"},
    "Bell Color": {"contado": 1789, "lista": 2260, "imagen": "https://storage.googleapis.com/scatone_proovedores/bellcolor.png", "moneda": "USD"},
    "Expocolor": {"contado": 2022.40, "lista": 2618.16, "imagen": "https://storage.googleapis.com/scatone_proovedores/expocolor.png", "moneda": "USD"},
    "Macavi": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Sherwin Williams": {"contado": 2027.26, "lista": 2438.55, "imagen": "https://storage.googleapis.com/scatone_proovedores/sherwin-williams.jpg", "moneda": "USD"},
}

datos_proveedor = {}
columnas_adicionales = []
widgets_dinamicos = []

def obtener_proveedores():
    return list(proveedores.keys())

def colocar_widgets_fijos(frame, columnas_dinamicas, precio_base_entry, resultado_contado, resultado_lista, cotizacion_label):
    """
    Posiciona los widgets fijos (Precio Base, Precios Calculados, Cotización) al final de las características dinámicas.
    """
    fila_base = len(columnas_dinamicas) + 6  # Determina la fila base en función de las características dinámicas

    # Precio Base
    ttk.Label(frame, text="Precio Base:", font=("Arial", 14)).grid(row=fila_base, column=0, pady=10, sticky=tk.W)
    precio_base_entry.grid(row=fila_base, column=1, pady=10, sticky=tk.W)

    # Resultados
    ttk.Label(frame, text="Precio Contado Efectivo:", font=("Arial", 14)).grid(row=fila_base + 1, column=0, pady=10, sticky=tk.W)
    ttk.Label(frame, textvariable=resultado_contado, font=("Arial", 14)).grid(row=fila_base + 1, column=1, pady=10, sticky=tk.W)

    ttk.Label(frame, text="Precio Lista:", font=("Arial", 14)).grid(row=fila_base + 2, column=0, pady=10, sticky=tk.W)
    ttk.Label(frame, textvariable=resultado_lista, font=("Arial", 14)).grid(row=fila_base + 2, column=1, pady=10, sticky=tk.W)

    # Cotización del dólar
    cotizacion_label.grid(row=fila_base + 3, column=0, columnspan=2, pady=20, sticky=tk.W)

def cargar_productos(proveedor_var, sheet, frame, imagen_proveedor_label, producto_dropdown, tipo_dropdown, precio_base_entry, resultado_contado, resultado_lista, cotizacion_label, producto_var, tipo_var, cotizacion):
    """
    Carga los productos del proveedor seleccionado y organiza los widgets dinámicamente.
    """
    proveedor_seleccionado = proveedor_var.get()
    if not proveedor_seleccionado:
        return

    try:
        # Limpiar los campos de precio al cambiar de proveedor
        precio_base_entry.delete(0, tk.END)
        resultado_contado.set("")
        resultado_lista.set("")
        print("Campos de precios limpiados al cambiar de proveedor.")

        # Limpiar widgets dinámicos previos
        global widgets_dinamicos
        for _, widget in widgets_dinamicos:
            widget.destroy()
        widgets_dinamicos.clear()

        # Actualizar imagen del proveedor
        if proveedor_seleccionado in proveedores:
            actualizar_imagen_proveedor(proveedores[proveedor_seleccionado]["imagen"], imagen_proveedor_label)

        # Leer datos del proveedor
        datos = leer_datos_hoja(sheet, proveedor_seleccionado)
        if not datos:
            messagebox.showwarning("Advertencia", f"No se encontraron datos para el proveedor {proveedor_seleccionado}.")
            return

        # Guardar datos del proveedor
        datos_proveedor[proveedor_seleccionado] = datos

        # Obtener columnas adicionales
        columnas = list(datos[0].keys())
        if not all(col in columnas for col in ["Producto", "Tipo", "Precio"]):
            messagebox.showerror("Error", f"Faltan columnas obligatorias en la hoja de {proveedor_seleccionado}.")
            return

        # Generar dropdown para productos
        productos = list(set(row["Producto"] for row in datos))
        producto_dropdown["values"] = productos
        producto_var.set("")  # Reiniciar producto seleccionado

        # Limpiar dropdowns de tipo y columnas adicionales
        tipo_dropdown["values"] = []
        tipo_var.set("")

        # Crear widgets dinámicos para columnas adicionales
        for i, columna in enumerate(columnas):
            if columna not in ["Producto", "Tipo", "Precio"]:
                ttk.Label(frame, text=f"{columna}:", font=("Arial", 14)).grid(row=6 + i, column=0, pady=5, sticky=tk.W)
                entry = ttk.Combobox(frame, font=("Arial", 14), state="readonly", width=40)
                entry.grid(row=6 + i, column=1, pady=5, sticky=tk.W)
                widgets_dinamicos.append((columna, entry))  # Guardar referencia al widget dinámico

        # Reorganizar widgets fijos
        colocar_widgets_fijos(frame, columnas, precio_base_entry, resultado_contado, resultado_lista, cotizacion_label)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos. Detalle: {e}")


def actualizar_tipos(proveedor_var, producto_var, frame, tipo_dropdown):
    """
    Actualiza los tipos según el producto seleccionado y muestra los datos correspondientes en las columnas dinámicas.
    """
    proveedor_seleccionado = proveedor_var.get()
    producto_seleccionado = producto_var.get()
    if not proveedor_seleccionado or not producto_seleccionado:
        return

    try:
        datos = datos_proveedor.get(proveedor_seleccionado, [])
        fila_producto = next((row for row in datos if row["Producto"] == producto_seleccionado), None)
        if not fila_producto:
            messagebox.showwarning("Advertencia", "No se encontró información para el producto seleccionado.")
            return

        # Actualizar el dropdown de tipos
        tipos = list(set(row["Tipo"] for row in datos if row["Producto"] == producto_seleccionado))
        tipo_dropdown["values"] = tipos
        tipo_dropdown.set("")

        # Actualizar widgets dinámicos según la fila seleccionada
        for columna, widget in widgets_dinamicos:
            valor_columna = fila_producto.get(columna, "")
            widget["values"] = [valor_columna] if valor_columna else []
            widget.set(valor_columna if valor_columna else "")

    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar los datos dinámicos. Detalle: {e}")

def cargar_precio(proveedor_var, producto_var, tipo_var, frame, precio_base_entry, resultado_contado, resultado_lista, cotizacion_label, cotizacion):
    """
    Calcula los precios según el proveedor, producto, tipo, y columnas dinámicas seleccionadas.
    """
    proveedor_seleccionado = proveedor_var.get()
    producto_seleccionado = producto_var.get()
    tipo_seleccionado = tipo_var.get()

    if not (proveedor_seleccionado and producto_seleccionado and tipo_seleccionado):
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los campos.")
        return

    try:
        # Obtener los datos del proveedor y la fila del producto/tipo
        datos = datos_proveedor.get(proveedor_seleccionado, [])
        fila_producto = next((row for row in datos if row["Producto"] == producto_seleccionado and row["Tipo"] == tipo_seleccionado), None)

        if not fila_producto:
            messagebox.showwarning("Advertencia", "No se encontró información para el producto seleccionado.")
            return

        # Obtener precio base y realizar conversión si es necesario
        precio_base = float(fila_producto.get("Precio", 0))
        moneda_proveedor = proveedores[proveedor_seleccionado].get("moneda", "ARS")
        if moneda_proveedor == "USD":
            precio_base *= cotizacion.get()  # Convertir a moneda local usando la cotización del dólar

        # Calcular precios contado y lista
        multiplicador_contado = proveedores[proveedor_seleccionado].get("contado", 1)
        multiplicador_lista = proveedores[proveedor_seleccionado].get("lista", 1)
        precio_contado = precio_base * multiplicador_contado
        precio_lista = precio_base * multiplicador_lista

        # Mostrar resultados en la interfaz
        precio_base_entry.delete(0, tk.END)
        precio_base_entry.insert(0, f"${precio_base:,.2f}")
        resultado_contado.set(f"${precio_contado:,.2f}")
        resultado_lista.set(f"${precio_lista:,.2f}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular el precio. Detalle: {e}")
