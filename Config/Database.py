import pyodbc
import logging
from Config.Senttings import DATABASE
logger = logging.getLogger(__name__)

class Database:
    """Gestión básica de conexión a SQL Server"""

    @staticmethod
    def get_connection():
        """
        Abre conexión bajo demanda.
        El cierre se maneja con 'with'.
        """
        try:
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER= {DATABASE.get('DB_SERVER')};"
                f"DATABASE={DATABASE.get('DB_NAME')};"
                f"UID={DATABASE.get('DB_USER')};"
                f"PWD={DATABASE.get('DB_PASSWORD')};"
                "TrustServerCertificate=yes;"
            )
            return conn

        except Exception:
            logger.error("Error conectando a SQL Server", exc_info=True)
            raise
DB=Database()
ejecucion=Database.get_connection()

print(ejecucion)