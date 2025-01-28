#google_sheets_module.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_google_sheets(credentials_file, sheet_name):
    """
    Establece conexión con Google Sheets utilizando credenciales y retorna la hoja seleccionada.
    """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name)
        return sheet
    except Exception as e:
        raise ConnectionError(f"Error al conectar con Google Sheets: {e}")

def leer_datos_hoja(sheet, hoja_nombre):
    """
    Lee los datos de una hoja específica y retorna una lista de diccionarios.
    """
    try:
        worksheet = sheet.worksheet(hoja_nombre)
        datos = worksheet.get_all_records()
        return datos
    except Exception as e:
        raise ValueError(f"Error al leer datos de la hoja '{hoja_nombre}': {e}")
