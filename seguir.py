import random
from time import sleep
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

# Esperar hasta que se cargue la página principal
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[text()="Inicio"]'))
)

# Lista de perfiles a seguir automáticamente
perfiles_a_seguir = ["perfil1", "perfil2", "perfil3"]  # Reemplaza con los perfiles deseados

# Contador de cuentas seguidas
contador = 0
limite = 20  # Límite máximo de cuentas a seguir

for perfil in perfiles_a_seguir:
    try:
        # Navegar al perfil
        driver.get(f"https://www.instagram.com/{perfil}/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button'))
        )

        # Buscar el botón de seguir
        follow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Seguir")]')

        # Verificar si ya se está siguiendo
        if "Siguiendo" in follow_button.text or "Following" in follow_button.text:
            print(f"Ya sigues a {perfil}.")
            continue

        # Hacer clic en "Seguir"
        follow_button.click()
        print(f"Seguiste a: {perfil}")

        # Incrementar el contador
        contador += 1

        # Verificar si se ha alcanzado el límite de cuentas a seguir
        if contador >= limite:
            print(f"Límite de {limite} cuentas alcanzado.")
            break

        # Simulación de comportamiento humano
        tiempo_espera = random.randint(5, 15)  # Pausa aleatoria entre 5 y 15 segundos
        print(f"Esperando {tiempo_espera} segundos antes de seguir la siguiente cuenta...")
        sleep(tiempo_espera)

    except Exception as e:
        print(f"No se pudo seguir a {perfil}: {e}")

# Cerrar el navegador después de completar
print("Proceso completado.")
driver.quit()
