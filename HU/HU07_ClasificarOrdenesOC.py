import win32com.client
import time
import subprocess
import re
from pathlib import Path
from Config.Senttings import SAP_CONFIG
from Funciones.ConexionSAP import ConexionSAP
from Funciones.consultarOC import consultarOC
from Config.init_config import in_config
from Repositorios.Excel import Excel as ExcelDB

class HU07_ClasificarOC:

    def __init__(self):
        """
        Inicializa la conexión a SAP y parámetros de tabla.
        """
        self.sap = ConexionSAP(
            SAP_CONFIG.get('SAP_USUARIO'),
            SAP_CONFIG.get('SAP_PASSWORD'),
            in_config('SAP_CLIENTE'),
            in_config('SAP_IDIOMA'),
            in_config('SAP_PATH'),
            in_config('SAP_SISTEMA')
        )
        
        self.sesion = None
        self.nombreTabla = "BaseMedicamentos"

    def ejecutar(self):
        """
        Extrae datos, limpia OCs, valida en SAP y clasifica en listas.
        """
        taskName = "HU07_ClasificarOC"
        
        # --- 1. INICIALIZACIÓN DE LISTAS DE CLASIFICACIÓN ---
        existeOC = []
        noExisteOC = []
        liberadaOC = []
        noLiberadaOC = []
        erroresTecnicos = []

        try:
            # 2. OBTENER REGISTROS DE LA DB
            print(f"Consultando registros pendientes en {self.nombreTabla}...")
            registros = ExcelDB.obtener_datos_por_posicion(self.nombreTabla)

            if not registros:
                print("No hay registros pendientes en la DB.")
                return

            # 3. INICIAR SESIÓN SAP
            self.sesion = self.sap.iniciar_sesion_sap()

            # 4. CICLO DE PROCESAMIENTO
            for registro in registros:
                oc_raw = str(registro.get('Orden2025', ''))
                cod_fin = registro.get('CodFin', 'N/A')

                # --- LIMPIEZA DE DATOS (REGEX) ---
                # Buscamos el patrón típico de OC (ej: empieza por 400 y tiene 10 dígitos)
                match = re.search(r'400\d{7}', oc_raw)
                
                if not match:
                    print(f"[-] Formato inválido o celda sucia: {oc_raw}")
                    noExisteOC.append(f"{oc_raw} (ID: {cod_fin})")
                    continue
                
                oc_numero = match.group(0)
                print(f"\n" + "-"*40)
                print(f"[*] Procesando OC limpia: {oc_numero} | CodFin: {cod_fin}")

                # --- VALIDACIÓN EN SAP ---
                # La función consultarOC debe retornar un dict: {"status": "OK/Error", "detalle": "..."}
                resultado = consultarOC(self.sesion, oc_numero)

                # --- CLASIFICACIÓN SEGÚN RESULTADO ---
                if resultado["status"] == "OK":
                    existeOC.append(oc_numero)
                    
                    # Lógica de liberación (basada en el texto que devuelve tu SAP)
                    if "liberada" in resultado["detalle"].lower() or "activ" in resultado["detalle"].lower():
                        print(f"[+] Orden Liberada")
                        liberadaOC.append(oc_numero)
                    else:
                        print(f"[!] Orden No Liberada")
                        noLiberadaOC.append(oc_numero)
                
                else:
                    # Manejo de "No existe" o errores de conexión
                    detalle_error = resultado["detalle"].lower()
                    if "no existe" in detalle_error:
                        print(f"[-] SAP informa: La orden no existe.")
                        noExisteOC.append(oc_numero)
                    else:
                        print(f"[x] Error Técnico: {resultado['detalle']}")
                        erroresTecnicos.append(oc_numero)

            # --- 5. RESUMEN FINAL DE EJECUCIÓN ---
            print("\n" + "="*50)
            print("            RESUMEN DE CLASIFICACIÓN")
            print("="*50)
            print(f"Total procesados: {len(registros)}")
            print(f"Existentes:       {len(existeOC)}")
            print(f"  - Liberadas:    {len(liberadaOC)}")
            print(f"  - No Liberadas: {len(noLiberadaOC)}")
            print(f"No Existen:       {len(noExisteOC)}")
            print(f"Errores Técnicos: {len(erroresTecnicos)}")
            print("="*50)

            # Opcional: Retornar las listas si otro proceso las necesita
            return {
                "liberadas": liberadaOC,
                "no_existe": noExisteOC,
                "errores": erroresTecnicos
            }

        except Exception as e:
            print(f"Falla critica en la clase HU07: {e}")
