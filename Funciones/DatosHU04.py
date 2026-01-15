import win32com.client  # Dependencia de pywin32 para interactuar con SAP
from datetime import datetime
import logging
import time

def consultar_datos_hu04(sesion, numeroOC):
    """
    Consulta la OC en SAP, extrae la fecha de creación y verifica historial de factura.
    """
    try:
        # Navegación a la transacción
        sesion.findById("wnd[0]/tbar[0]/okcd").text = "/nME23N"
        sesion.findById("wnd[0]").sendVKey(0)
        
        time.sleep(1)
        # Cargar el número de Orden
        sesion.findById("wnd[0]/tbar[1]/btn[17]").press()
        sesion.findById("wnd[1]/usr/subSUB0:SAPLMEGUI:0003/ctxtMEPO_SELECT-EBELN").text = str(numeroOC)
        sesion.findById("wnd[1]").sendVKey(0)
        
        # 1. Obtener Fecha de Creación (Cabecera -> Pestaña Datos Org. o similar según tu Layout)
        # Ajustamos el ID al campo de fecha de documento (BEDAT)
        fecha_raw = sesion.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0015/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/ctxtMEPO_TOPLINE-BEDAT").text
        fecha_creacion = datetime.strptime(fecha_raw, "%d.%m.%Y")
        dias_mora = (datetime.now() - fecha_creacion).days

        # 2. Revisar Historial de Pedido
        facturada = False
        try:
            # Seleccionar pestaña Historial (T7)
            sesion.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0015/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT13").select()
            grid = sesion.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0010/subSUB3:SAPLMEGUI:0020/subSUB1:SAPLMEGUI:0032/tabsTABSTRIP_LINE/tabpT\07/ssubSUB0:SAPLMEGUI:0071/cntlGRIDCONTROL/shellcont/shell")
            
            for i in range(grid.RowCount):
                # Buscamos 'RE-L' o 'Factura'
                if grid.getCellValue(i, "BEZTP") in ["RE-L", "Factura"]:
                    facturada = True
                    break
        except:
            # Si no hay pestaña de historial, no hay factura
            facturada = False

        return {
            "status": "OK",
            "fecha_sap": fecha_creacion.strftime("%Y-%m-%d"),
            "dias": dias_mora,
            "facturada": facturada
        }
    except Exception as e:
        return {"status": "Error", "detalle": str(e)}