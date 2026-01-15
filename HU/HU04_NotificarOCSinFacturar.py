import pandas as pd
import glob
import time
import os
from datetime import datetime
from Funciones.DatosHU04 import consultar_datos_hu04
from Funciones.ConexionSAP import ConexionSAP
from Config.Senttings import SAP_CONFIG
from Config.init_config import in_config

class HU04_Auditoria:
    def __init__(self):
        self.sap = ConexionSAP(
            SAP_CONFIG.get('SAP_USUARIO'),
            SAP_CONFIG.get('SAP_PASSWORD'),
            in_config('SAP_CLIENTE'),
            in_config('SAP_IDIOMA'),
            in_config('SAP_PATH'),
            in_config('SAP_SISTEMA')
        )
        self.sesion = None
        self.ruta_input = r"\\192.168.50.169\RPA_RIGO_GestionPagodeArrendamientos\Resultados"
        self.ruta_output = r"\\192.168.50.169\RPA_RIGO_GestionPagodeArrendamientos\Resultados\Reportes_HU04"

    def buscar_ultimo_reporte_hu07(self):
        archivos = glob.glob(os.path.join(self.ruta_input, "Reporte_Gestion_HU07_20260115_1057.xlsx"))
        return max(archivos, key=os.path.getctime) if archivos else None

    def ejecutar(self):
        # 1. INICIAR SESIÓN UNA SOLA VEZ
        print(">>> Conectando a SAP para Auditoría HU04...")
        self.sesion = self.sap.iniciar_sesion_sap()
        
        # Validación de seguridad: Si no hay sesión, no intentamos nada más
        if not self.sesion:
            print("[-] Error crítico: No se pudo iniciar sesión en SAP. Abortando.")
            return

        time.sleep(2) # Tiempo de gracia para que cargue la interfaz

        # 2. BUSCAR EL INSUMO (REPORTE HU07)
        archivo_hu07 = self.buscar_ultimo_reporte_hu07()
        if not archivo_hu07:
            print("[-] No se encontró ningún reporte de la HU07 en la ruta de red.")
            return

        print(f">>> Leyendo reporte HU07: {os.path.basename(archivo_hu07)}")
        df_hu07 = pd.read_excel(archivo_hu07)

        # 3. FILTRAR REGISTROS VÁLIDOS
        ocs_para_auditar = df_hu07[df_hu07['Estado SAP'].isin(['Liberada', 'Pendiente Liberación'])]
        
        if ocs_para_auditar.empty:
            print("[!] El reporte no tiene OCs para auditar.")
            return

        resultados_auditoria = []

        # 4. CICLO DE AUDITORÍA (Usamos la sesión ya abierta)
        print(f"\n>>> Iniciando auditoría de {len(ocs_para_auditar)} órdenes...")
        
        for _, fila in ocs_para_auditar.iterrows():
            oc = str(fila['OC'])
            print(f"[*] Procesando OC {oc}...")

            # Llamamos a la función de consulta (Asegúrate que use la ME23N o ME2L)
            res = consultar_datos_hu04(self.sesion, oc)
            
            if res["status"] == "OK":
                # Lógica: Si pasaron 2 días o más y no está facturada, requiere acción
                es_critico = res["dias"] >= 2 and not res["facturada"]
                
                resultados_auditoria.append({
                    "OC": oc,
                    "Proveedor": fila['Proveedor'],
                    "Monto": fila['Monto'],
                    "Fecha Creación SAP": res["fecha_sap"],
                    "Días de Antigüedad": res["dias"],
                    "Tiene Factura": "SÍ" if res["facturada"] else "NO",
                    "Requiere Acción": "SÍ" if es_critico else "NO"
                })
            else:
                print(f"    [!] Error al leer datos de la OC {oc}: {res['detalle']}")

        # 5. GENERAR INFORME FINAL
        self.guardar_informe(resultados_auditoria)

    def guardar_informe(self, datos):
        if not datos: return
        df_final = pd.DataFrame(datos)
        
        # Si no existe la carpeta, la creamos
        if not os.path.exists(self.ruta_output):
            os.makedirs(self.ruta_output)
            
        nombre = f"Informe_Auditoria_Facturacion_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        df_final.to_excel(os.path.join(self.ruta_output, nombre), index=False)
        print(f"\n[!] AUDITORÍA FINALIZADA. Informe generado: {nombre}")

# --- DIAGRAMA DEL PROCESO ACTUAL ---
#