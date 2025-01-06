from flask import Flask, render_template, request
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import threading
import os


app = Flask(__name__)

# Variable global para controlar el estado del bot
bot_active = False
driver = None
username = ""
password = ""
followed_count = 0  # Contador de cuentas seguidas

@app.route('/')
def index():
    return render_template('index.html', followed_count=followed_count)

@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot_active, driver, username, password, followed_count

    # Obtener los datos de login desde el formulario
    username = request.form.get('username')
    password = request.form.get('password')

    if bot_active:
        return "El bot ya está en ejecución."

    # Marcar el bot como activo
    bot_active = True
    followed_count = 0  # Reiniciar el contador al iniciar el bot

    # Iniciar el bot en un hilo separado para no bloquear la aplicación web
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    return "Bot iniciado con éxito."

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global bot_active, driver

    if not bot_active:
        return "El bot no está en ejecución."

    # Marcar el bot como inactivo
    bot_active = False

    # Cerrar el navegador si está abierto
    if driver:
        driver.quit()

    return "Bot detenido con éxito."

def run_bot():
    global bot_active, driver, username, password, followed_count

    # Configuración de opciones de Chrome
    options = Options()
    options.add_argument("--incognito")

    # Crear el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())
    service.keep_alive = True

    # Crear el navegador
    driver = webdriver.Chrome(service=service, options=options)

    # Iniciar sesión en Instagram
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

    # Escribir nombre de usuario y contraseña obtenidos del formulario
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Hacer clic en el botón de login
    login_button.click()

    # Esperar hasta que se cargue la página principal
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="Inicio"]'))  # Elemento visible en la página de inicio
        )
        print("Inicio de sesión exitoso.")
    except Exception as e:
        # Si no se encuentra el elemento esperado o se presenta un error
        print(f"Error al iniciar sesión: {e}")
        # Verificar si aparece un mensaje de error en la página
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"incorrecto")]'))  # Mensaje de error en caso de credenciales incorrectas
            )
            print("Credenciales incorrectas o cuenta bloqueada.")
        except Exception:
            print("Error desconocido en el inicio de sesión.")
        driver.quit()
        bot_active = False
        return

    # Si se llegó a este punto, el inicio de sesión fue exitoso y se puede proceder con el bot

    # Explorar y seguir perfiles automáticamente desde el feed
    contador = 0
    limite = 20  # Límite máximo de cuentas a seguir

    while bot_active and contador < limite:
        try:
            # Cargar más posts en el feed si es necesario
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//article//a'))
            )

            # Encontrar un perfil en el feed
            posts = driver.find_elements(By.XPATH, '//article//a')
            if not posts:
                print("No se han encontrado posts para explorar.")
                break

            # Elegir un perfil aleatorio del feed
            perfil = random.choice(posts).get_attribute("href").split('/')[-2]

            # Verificar si ya se está siguiendo
            driver.get(f"https://www.instagram.com/{perfil}/")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button'))
            )

            follow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Seguir")]')

            if "Siguiendo" in follow_button.text or "Following" in follow_button.text:
                print(f"Ya sigues a {perfil}.")
                continue

            # Hacer clic en "Seguir"
            follow_button.click()
            print(f"Seguiste a: {perfil}")

            # Incrementar el contador
            followed_count += 1
            print(f"Cuentas seguidas: {followed_count}")

            # Simulación de comportamiento humano
            tiempo_espera = random.randint(5, 15)  # Pausa aleatoria entre 5 y 15 segundos
            print(f"Esperando {tiempo_espera} segundos antes de seguir la siguiente cuenta...")
            sleep(tiempo_espera)

        except Exception as e:
            print(f"Error al seguir a un perfil: {e}")
            continue
    # Cerrar el navegador después de completar
    print("Proceso completado.")
    driver.quit()
    bot_active = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
