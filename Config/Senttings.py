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

}



# Configuración del proceso

DATABASE = {
    'DB_SERVER': os.getenv('DB_SERVER'),
    'DB_NAME': os.getenv('DB_NAME'),
    'DB_USER': os.getenv('DB_USER'),
    'DB_PASSWORD': os.getenv('DB_PASSWORD')
}