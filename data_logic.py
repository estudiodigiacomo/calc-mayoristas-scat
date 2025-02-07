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
    "Sherwin Williams": {"contado": 2027.26, "lista": 2438.55, "imagen": "https://storage.googleapis.com/scatone_proovedores/sherwin-williams.jpg", "moneda": "USD"},
    "Expocolor": {"contado": 2022.40, "lista": 2618.16, "imagen": "https://storage.googleapis.com/scatone_proovedores/expocolor.png", "moneda": "USD"},
    "Macavi Raros": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Epoxi": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Automotor": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Poliuretanos Linea Especial": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Tenax Plastificantes": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Esmalte Flash": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Acrilito Adherente": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Selladores y Lacas Tintas": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Barnices Impregnantes Deck": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Sinteticos": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Horneables": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Duatlon": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Antioxido": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},
    "Macavi Diluyentes": {"contado": 1318.54, "lista": 2009.34, "imagen": "https://storage.googleapis.com/scatone_proovedores/macavi.jpg", "moneda": "USD"},

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

    # Resultados
    ttk.Label(frame, text="Precio Contado Efectivo:", font=("Arial", 14)).grid(row=fila_base + 1, column=0, pady=10, sticky=tk.W)
    ttk.Label(frame, textvariable=resultado_contado, font=("Arial", 14)).grid(row=fila_base + 1, column=1, pady=10, sticky=tk.W)

    ttk.Label(frame, text="Precio Lista:", font=("Arial", 14)).grid(row=fila_base + 2, column=0, pady=10, sticky=tk.W)
    ttk.Label(frame, textvariable=resultado_lista, font=("Arial", 14)).grid(row=fila_base + 2, column=1, pady=10, sticky=tk.W)

    # Cotización del dólar
    cotizacion_label.grid(row=fila_base + 3, column=0, columnspan=2, pady=20, sticky=tk.W)

def cargar_productos(proveedor_var, sheet, frame, imagen_proveedor_label, producto_dropdown, tipo_dropdown, medida_dropdown, color_dropdown, resultado_contado, resultado_lista, cotizacion_label, producto_var, tipo_var, medida_var, color_var, cotizacion):
    """
    Carga los productos del proveedor seleccionado y actualiza los dropdowns de Producto, Tipo, Medida y Color.
    """
    proveedor_seleccionado = proveedor_var.get()
    if not proveedor_seleccionado:
        return

    try:
        # Limpiar campos al cambiar de proveedor
        producto_dropdown["values"] = []
        tipo_dropdown["values"] = []
        medida_dropdown["values"] = []
        color_dropdown["values"] = []
        producto_var.set("")
        tipo_var.set("")
        medida_var.set("")
        color_var.set("")
        resultado_contado.set("")
        resultado_lista.set("")

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

        # Verificar columnas obligatorias
        columnas_necesarias = ["Producto", "Tipo", "Medida o Cantidad", "Precio"]
        if not all(col in datos[0] for col in columnas_necesarias):
            messagebox.showerror("Error", f"Faltan columnas obligatorias en la hoja de {proveedor_seleccionado}.")
            return

        # Generar lista de productos
        productos = sorted(set(row["Producto"] for row in datos))
        producto_dropdown["values"] = productos

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos. Detalle: {e}")


def actualizar_tipos(proveedor_var, producto_var, tipo_dropdown, medida_dropdown, color_dropdown, tipo_var, medida_var, color_var):
    """
    Actualiza los valores de Tipo, Medida o Cantidad y Color (si existe) según el Producto seleccionado.
    """
    proveedor_seleccionado = proveedor_var.get()
    producto_seleccionado = producto_var.get()

    if not proveedor_seleccionado or not producto_seleccionado:
        return

    try:
        datos = datos_proveedor.get(proveedor_seleccionado, [])

        # Filtrar tipos según el producto seleccionado
        tipos_disponibles = sorted(set(row["Tipo"] for row in datos if row["Producto"] == producto_seleccionado))
        tipo_dropdown["values"] = tipos_disponibles
        tipo_var.set("")  # Resetear el tipo seleccionado

        # Detectar si la columna "Color" está presente
        columna_color_presente = "Color" in datos[0]

        def actualizar_medidas_y_colores(event=None):
            tipo_seleccionado = tipo_var.get()

            # Filtrar medidas según producto y tipo
            medidas_disponibles = sorted(
                set(
                    row["Medida o Cantidad"]
                    for row in datos
                    if row["Producto"] == producto_seleccionado and row["Tipo"] == tipo_seleccionado
                )
            )
            medida_dropdown["values"] = medidas_disponibles
            medida_var.set("")  # Resetear medida seleccionada

            # Solo cargar colores si la columna existe
            if columna_color_presente:
                colores_disponibles = sorted(
                    set(
                        row["Color"]
                        for row in datos
                        if row["Producto"] == producto_seleccionado and row["Tipo"] == tipo_seleccionado
                    )
                )
                color_dropdown["values"] = colores_disponibles
                color_var.set("")  # Resetear color seleccionado
                color_dropdown.grid()  # Asegurar que se muestre
            else:
                color_dropdown["values"] = []
                color_var.set("")
                color_dropdown.grid_remove()  # Ocultar el dropdown

        # Asociar el evento al dropdown de tipo
        tipo_dropdown.bind("<<ComboboxSelected>>", actualizar_medidas_y_colores)

        # Limpiar dropdowns de medida y color si no hay tipo seleccionado
        medida_dropdown["values"] = []
        medida_var.set("")
        color_dropdown["values"] = []
        color_var.set("")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar los datos. Detalle: {e}")

def limpiar_formato_monetario(valor):
    """
    Convierte un valor con formato monetario a un número flotante.
    Ejemplo: "$ 98.963,09" -> 98963.09
    """
    if isinstance(valor, str):
        # Elimina el símbolo de moneda y los separadores de miles
        valor = valor.replace("$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(valor)
    except ValueError:
        raise ValueError(f"Error al convertir el valor '{valor}' a float.")


def cargar_precio(proveedor_var, producto_var, tipo_var, medida_var, color_var, resultado_contado, resultado_lista, cotizacion):
    """
    Obtiene y muestra el precio según el producto, tipo, medida y color (si aplica) seleccionados.
    """
    proveedor_seleccionado = proveedor_var.get()
    producto_seleccionado = producto_var.get()
    tipo_seleccionado = tipo_var.get()
    medida_seleccionada = medida_var.get()

    datos = datos_proveedor.get(proveedor_seleccionado, [])
    columna_color_presente = "Color" in datos[0] if datos else False

    # Verificar los campos obligatorios (Color no será obligatorio)
    if not (proveedor_seleccionado and producto_seleccionado and tipo_seleccionado and medida_seleccionada):
        messagebox.showwarning("Advertencia", "Por favor, seleccione todos los campos.")
        return

    try:
        # Filtrar la fila exacta según los parámetros disponibles
        fila_producto = next(
            (row for row in datos
             if row["Producto"] == producto_seleccionado
             and row["Tipo"] == tipo_seleccionado
             and row["Medida o Cantidad"] == medida_seleccionada
             and (not columna_color_presente or row.get("Color") == color_var.get())),
            None
        )

        if not fila_producto:
            resultado_contado.set("")
            resultado_lista.set("")
            return

        # Obtener y limpiar el precio base
        precio_base = limpiar_formato_monetario(fila_producto["Precio"])
        precio_contado = precio_base * proveedores[proveedor_seleccionado]["contado"]
        precio_lista = precio_base * proveedores[proveedor_seleccionado]["lista"]

        # Actualizar los resultados
        resultado_contado.set(f"${precio_contado:,.2f}")
        resultado_lista.set(f"${precio_lista:,.2f}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular el precio. Detalle: {e}")

