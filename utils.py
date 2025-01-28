#utils.py
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import io

def obtener_cotizacion_dolar(cotizacion_var, cotizacion_label):
    try:
        api_url = "https://dolarapi.com/v1/dolares/oficial"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if "venta" in data:
                cotizacion_var.set(float(data["venta"]))
                cotizacion_label.config(text=f"Cotización utilizada: ${data['venta']:,.2f}")
        else:
            raise ValueError("API no devolvió un estado válido.")

    except Exception as e:
        cotizacion_var.set(0.0)
        cotizacion_label.config(text="Cotización no disponible")
        messagebox.showerror("Error", f"No se pudo obtener la cotización. Detalle: {e}")

def actualizar_imagen_proveedor(imagen_url, imagen_proveedor_label):
    try:
        response = requests.get(imagen_url, stream=True)
        if response.status_code == 200:
            img_data = io.BytesIO(response.content)
            img = Image.open(img_data).resize((200, 200), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            imagen_proveedor_label.config(image=img_tk)
            imagen_proveedor_label.image = img_tk
        else:
            raise ValueError("Error al cargar imagen.")
    except Exception as e:
        imagen_proveedor_label.config(image="", text="Sin imagen")
        print(f"Error al cargar imagen: {e}")
