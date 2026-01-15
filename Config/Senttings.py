# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración SAP
SAP_CONFIG = {
    'SAP_USUARIO': os.getenv('SAP_USUARIO'),
    'SAP_PASSWORD': os.getenv('SAP_PASSWORD'),
    'SAP_CLIENTE': os.getenv('SAP_CLIENTE'),
    'SAP_IDIOMA': os.getenv('SAP_IDIOMA', 'ES'),
    'SAP_PATH': os.getenv('SAP_PATH'),
    'SAP_SISTEMA': os.getenv('SAP_SISTEMA')
}

# Rutas del proyecto
RUTAS = {
    'PATH_PROYECTO': os.getenv('PATH_PROYECTO', 'C:/ProgramData/RIGO'),
    'PATH_AUDIT': os.getenv('PATH_AUDIT', 'C:/ProgramData/RIGO/Audit'),
    'PATH_LOGS': os.getenv('PATH_LOGS', 'C:/ProgramData/RIGO/Audit/Logs'),
    'PATH_TEMP': os.getenv('PATH_TEMP', 'C:/ProgramData/RIGO/Temp'),
    'PATH_INSUMO': os.getenv('PATH_INSUMO', 'C:/ProgramData/RIGO/Insumo'),
    'PATH_RESULTADO': os.getenv('PATH_RESULTADO', 'C:/ProgramData/RIGO/Resultado')
}

# Configuración del proceso
PROCESO_CONFIG = {
    'DIAS_ESPERA_LIBERACION': 2,
    'HORA_LIMITE_ENVIO': '11:45',
    'MAX_REINTENTOS_SAP': 3,
    'TIMEOUT_SAP': 30
}

# Validar que SAP_PATH existe
if SAP_CONFIG['SAP_PATH'] and not Path(SAP_CONFIG['SAP_PATH']).exists():
    print(f"⚠️  ADVERTENCIA: SAP GUI no encontrado en: {SAP_CONFIG['SAP_PATH']}")

DATABASE = {
    'DB_SERVER': os.getenv('DB_SERVER'),
    'DB_NAME': os.getenv('DB_NAME'),
    'DB_USER': os.getenv('DB_USER'),
    'DB_PASSWORD': os.getenv('DB_PASSWORD')
}