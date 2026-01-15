from Repositorios.Excel import Excel
from HU.HU07_ClasificarOrdenesOC import HU07_ClasificarOC
from HU.HU04_NotificarOCSinFacturar import HU04_Auditoria

if __name__ == "__main__":
    """pruebaExcel=HU07_ClasificarOC()
    pruebaExcel.ejecutar()"""

    ejecucionHu04=HU04_Auditoria()
    ejecucionHu04.ejecutar()
    