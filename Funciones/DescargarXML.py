from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def abrir_web(ruta="https://colsubsidio.efacturacadena.com/"):
    opciones = Options()
    opciones.add_argument("--start-maximized") 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opciones)
    driver.get(ruta) 
    
    return driver

# Ejecución
mi_navegador = abrir_web()
def descargar_XML(usuario, contraseña):
    pass


ruta="https://colsubsidio.efacturacadena.com/"
abrir_web(ruta)