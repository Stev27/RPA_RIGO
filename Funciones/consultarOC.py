import win32com.client  # Para SAP
import pandas as pd     # Para la lógica de negocio y Excel
import os    
import time           # Para rutas del File Server
from datetime import datetime, timedelta
from Funciones.ConexionSAP import ConexionSAP
from Config.Senttings import SAP_CONFIG
from Config.init_config import in_config

def consultarOC(sesion, numeroOC):
    
    try:
        # Navegación
        sesion.findById("wnd[0]/tbar[0]/okcd").text = "/nME23N"
        sesion.findById("wnd[0]").sendVKey(0)
        
        sesion.findById("wnd[0]/tbar[1]/btn[17]").press()
        sesion.findById("wnd[1]/usr/subSUB0:SAPLMEGUI:0003/ctxtMEPO_SELECT-EBELN").text = str(numeroOC)
        sesion.findById("wnd[1]").sendVKey(0)
        
        # Validación de Barra de Estado
        mensaje_sap = sesion.findById("wnd[0]/sbar").text
        tipo_mensaje = sesion.findById("wnd[0]/sbar").messagetype 

        if tipo_mensaje == "E":
            if sesion.Children.Count > 1:
                sesion.findById("wnd[1]").sendVKey(12) # Cerrar popup
            # IMPORTANTE: Devolver diccionario
            return {"status": "Error", "detalle": mensaje_sap}
        
        # Si todo sale bien
        return {"status": "OK", "detalle": "Orden cargada exitosamente"}

    except Exception as e:
        return {"status": "Error", "detalle": str(e)}