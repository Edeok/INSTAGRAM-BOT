from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configuración de opciones de Chrome
options = Options()
options.add_argument("--incognito")

# Crear el servicio de ChromeDriver
service = Service(ChromeDriverManager().install())
service.keep_alive = True

# Crear el navegador
driver = webdriver.Chrome(service=service, options=options)

# Acceder a Instagram
driver.get("http://www.instagram.com")

# Esperar hasta que los campos de username y password estén disponibles
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input'))
)
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input'))
)
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]'))
)

# Escribir nombre de usuario y contraseña
username_input.send_keys("usuario")
password_input.send_keys("contraseña")

# Hacer clic en el botón de login
login_button.click()

# Mantener el navegador abierto para depuración
input("Presiona Enter para cerrar el navegador...")
driver.quit()
