


import logging
from pathlib import Path
from datetime import datetime
from Config.init_config import init_config, in_config

class Reutilizables:
    """Clase para manejo de ambiente y logging del proyecto"""
    
    def __init__(self, path_proyecto, path_audit, path_logs, path_temp, path_insumo, path_resultado):
        self.path_proyecto = Path(path_proyecto)
        self.path_audit = Path(path_audit)
        self.path_logs = Path(path_logs)
        self.path_temp = Path(path_temp)
        self.path_insumo = Path(path_insumo)
        self.path_resultado = Path(path_resultado)


    def crear_carpetas(self):
            """Crea todas las carpetas necesarias para el proyecto"""
            try:
                carpetas = {
                    'Proyecto': self.path_proyecto,
                    'Auditoría': self.path_audit,
                    'Logs': self.path_logs,
                    'Temporal': self.path_temp,
                    'Insumos': self.path_insumo,
                    'Resultados': self.path_resultado
                }
                
                for nombre, carpeta in carpetas.items():
                    if not carpeta.exists():
                        carpeta.mkdir(parents=True, exist_ok=True)
                        self.logger.info(f"✓ Carpeta creada: {nombre} -> {carpeta}")
                    else:
                        self.logger.debug(f"Carpeta ya existe: {nombre} -> {carpeta}")
                
                self.logger.info("Despliegue de ambiente completado exitosamente")
                return True
                
            except Exception as e:
                self.logger.error(f"Error al crear carpetas: {str(e)}", exc_info=True)
                return False
    
    def audit_log(self, mensaje, tipo='INFO'):
        """Log de auditoría"""
        if tipo == 'INFO':
            self.logger.info(mensaje)
        elif tipo == 'WARNING':
            self.logger.warning(mensaje)
        elif tipo == 'ERROR':
            self.logger.error(mensaje)
        elif tipo == 'DEBUG':
            self.logger.debug(mensaje)
    
    def limpiar_carpeta_temp(self):
        """Limpia archivos temporales"""
        try:
            archivos_eliminados = 0
            for archivo in self.path_temp.glob('*'):
                if archivo.is_file():
                    archivo.unlink()
                    archivos_eliminados += 1
            
            self.logger.info(f"Carpeta temporal limpiada. {archivos_eliminados} archivos eliminados")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al limpiar carpeta temporal: {str(e)}")
            return False
    
    def validar_archivo_existe(self, ruta_archivo):
        """Valida si un archivo existe"""
        archivo = Path(ruta_archivo)
        if archivo.exists():
            self.logger.debug(f"Archivo encontrado: {archivo.name}")
            return True
        else:
            self.logger.warning(f"Archivo NO encontrado: {archivo}")
            return False
    
    def get_ruta_insumo(self, nombre_archivo):
        """Obtiene ruta completa de archivo en carpeta insumo"""
        return self.path_insumo / nombre_archivo
    
    def get_ruta_resultado(self, nombre_archivo):
        """Obtiene ruta completa de archivo en carpeta resultado"""
        return self.path_resultado / nombre_archivo
    
    def get_ruta_temp(self, nombre_archivo):
        """Obtiene ruta completa de archivo en carpeta temp"""
        return self.path_temp / nombre_archivo
    
    def cargar_configuracion():
        init_config()
        print("In_config cargado:", in_config("PathProyecto"))
        print("Configuracion global iniciada")