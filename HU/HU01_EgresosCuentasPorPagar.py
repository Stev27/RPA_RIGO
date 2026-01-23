from Funciones.ConexionSAP import ConexionSAP
from Funciones.LeerXML import LectorFacturaXML
from Funciones.ME2L import TransaccionME2L
from Funciones.MIGO import TransaccionMIGO
from Config.Senttings import SAP_CONFIG, CADENA
from Config.init_config import in_config
from Funciones.DescargarXML import login_colsubsidio, realizar_consulta, descargar_xml_final


class Facturas:
    def __init__(self):
        self.sap=ConexionSAP(
            SAP_CONFIG.get('SAP_USUARIO'),
            SAP_CONFIG.get('SAP_PASSWORD'),
            in_config('SAP_CLIENTE'),
            in_config('SAP_IDIOMA'),
            in_config('SAP_PATH'),
            in_config('SAP_SISTEMA')
        )
        self.sesion = None

        self.cadenaUsuario=CADENA.get('CADENA_USUARIO')
        self.cadenaContraseña=CADENA.get('CADENA_CONTRASEÑA')
        self.cadenaRuta=CADENA.get('CADENA_RUTA')

    def descargar_XML(self):
        pass




def main():
    # 1. Conexión
    sap = ConexionSAP(
                SAP_CONFIG.get('SAP_USUARIO'),
                SAP_CONFIG.get('SAP_PASSWORD'),
                in_config('SAP_CLIENTE'),
                in_config('SAP_IDIOMA'),
                in_config('SAP_PATH'),
                in_config('SAP_SISTEMA')
            )
    sap.iniciar_sesion_sap()
    
    # 2. Leer XML (Suponiendo que está en tu carpeta de Insumos)
    xml_path = r"C:\ProgramData\RIGO\Insumo\ad090063145002525021701C7.xml"
    datos = LectorFacturaXML(xml_path).obtener_datos()
    
    # 3. Buscar OC
    me2l = TransaccionME2L(sap)
    oc = me2l.buscar_oc_activa(datos['nit'])
    
    # 4. Registrar MIGO
    if oc:
        migo = TransaccionMIGO(sap)
        migo.contabilizar_entrada(oc, datos['factura'])