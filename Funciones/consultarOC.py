import win32com.client  # Para SAP
import pandas as pd     # Para la lógica de negocio y Excel
import os               # Para rutas del File Server
from datetime import datetime, timedelta
from Funciones.ConexionSAP import ConexionSAP

def consultarOC(sesion, numeroOC):
    # validar ordenes de compra
    sesion.findById("wnd[0]/tbar[0]/okcd").text = f"/ME23N" 
    sesion.findById("wnd[0]").sendVKey(0)

    sesion.findById("wnd[0]/tbar[1]/btn[17]").press() # Botón 'Otra orden'
    sesion.findById("wnd[1]/usr/subSUB0:SAPLMEGUI:0003/ctxtMEPO_SELECT-EBELN").text = numeroOC
    sesion.findById("wnd[1]").sendVKey(0)

    estado = sesion.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0010/...").text 
    return estado