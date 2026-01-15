import pandas as pd
import glob
import os
from datetime import datetime
from Funciones.DatosHU04 import consultar_datos_hu04

class HU04_Auditoria:
    def __init__(self, sap_sesion):
        self.sesion = sap_sesion
        self.ruta_input = r"C:\RPA_RIGO\Reportes"
        self.ruta_output = r"C:\RPA_RIGO\Reportes_HU04"

    def buscar_ultimo_reporte_hu07(self):
        archivos = glob.glob(os.path.join(self.ruta_input, "Reporte_Gestion_HU07_*.xlsx"))
        return max(archivos, key=os.path.getctime) if archivos else None

    def ejecutar(self):
        archivo_hu07 = self.buscar_ultimo_reporte_hu07()
        if not archivo_hu07:
            print("No se encontró reporte de la HU07 para auditar.")
            return

        print(f">>> Leyendo reporte HU07: {os.path.basename(archivo_hu07)}")
        df_hu07 = pd.read_excel(archivo_hu07)

        # Filtramos solo las que la HU07 confirmó que existen
        ocs_para_auditar = df_hu07[df_hu07['Estado SAP'].isin(['Liberada', 'Pendiente Liberación'])]
        
        resultados_auditoria = []

        for _, fila in ocs_para_auditar.iterrows():
            oc = str(fila['OC'])
            print(f"[*] Auditando OC {oc}...")
            
            res = consultar_datos_hu04(self.sesion, oc)
            
            if res["status"] == "OK":
                # Determinamos si es un pendiente crítico
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

        # Generar Informe Final
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