from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pytest

# Credenciales para pruebas
USERNAME = "kayinik518@idoidraw.com"
CORRECT_PASSWORD = "C4ll!!m3"
INCORRECT_PASSWORD = "wrong_password"

# Función auxiliar para intentar login
def attempt_login(driver, username, password):
    """Intenta iniciar sesión con las credenciales dadas"""
    # Asegurarse de estar en la página de login
    if "auth/login" not in driver.current_url:
        driver.get("https://practicesoftwaretesting.com/auth/login")
        sleep(1)
    
    # Localizar e introducir username
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(username)
    
    # Localizar e introducir password
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    
    # Localizar el botón y hacer click
    driver.find_element(By.XPATH, '//input[@data-test="login-submit"]').click()
    sleep(1)

# Caso positivo 1: El usuario ingresa correctamente desde el primer intento
def test_successful_login_first_attempt():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Intentar login con credenciales correctas
    attempt_login(driver, USERNAME, CORRECT_PASSWORD)
    
    # Verificar que se ha accedido correctamente
    assert "account" in driver.current_url
    
    driver.quit()

# Caso positivo 2: El usuario ingresa mal la contraseña 2 veces, pero en el tercer intento lo hace correctamente
def test_successful_login_after_two_failures():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Primer intento fallido
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    
    # Segundo intento fallido
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    
    # Tercer intento correcto
    attempt_login(driver, USERNAME, CORRECT_PASSWORD)
    
    # Verificar que se ha accedido correctamente
    assert "account" in driver.current_url
    
    driver.quit()

# Caso positivo 3: Usar un usuario diferente después de fallar con otro
def test_successful_login_different_user():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Tres intentos fallidos con un usuario
    attempt_login(driver, "wrong_user@example.com", INCORRECT_PASSWORD)
    attempt_login(driver, "wrong_user@example.com", INCORRECT_PASSWORD)
    attempt_login(driver, "wrong_user@example.com", INCORRECT_PASSWORD)
    
    # Intento exitoso con el usuario correcto
    attempt_login(driver, USERNAME, CORRECT_PASSWORD)
    
    # Verificar que se ha accedido correctamente
    assert "account" in driver.current_url
    
    driver.quit()

# Caso negativo 1: El usuario falla 3 veces seguidas y queda bloqueado
def test_account_locked_after_three_failures():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Tres intentos fallidos consecutivos
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    
    # Cuarto intento con contraseña correcta, pero usuario ya bloqueado
    attempt_login(driver, USERNAME, CORRECT_PASSWORD)
    
    # Verificar mensaje de error que indica que la cuenta está bloqueada
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "locked" in error_message.lower()
    
    driver.quit()

# Caso negativo 2: El usuario se equivoca 2 veces, espera unos segundos y falla una tercera vez
def test_account_locked_with_delay_between_attempts():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Dos intentos fallidos consecutivos
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    
    # Esperar unos segundos
    sleep(5)
    
    # Tercer intento fallido
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    
    # Cuarto intento con contraseña correcta, pero el usuario ya está bloqueado
    attempt_login(driver, USERNAME, CORRECT_PASSWORD)
    
    # Verificar mensaje de error que indica que la cuenta está bloqueada
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "locked" in error_message.lower()
    
    driver.quit()

# Caso negativo 3: Intentar acceder con un usuario bloqueado (tras realizar 3 intentos fallidos)
def test_attempt_login_to_previously_locked_user():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Bloquear la cuenta con tres intentos fallidos
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    attempt_login(driver, USERNAME, INCORRECT_PASSWORD)
    
    # Cerrar el navegador y abrir uno nuevo (simular nuevo acceso)
    driver.quit()
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com/auth/login")
    
    # Intentar acceder con el usuario ahora bloqueado
    attempt_login(driver, USERNAME, CORRECT_PASSWORD)
    
    # Verificar mensaje de error que indica que la cuenta está bloqueada
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "locked" in error_message.lower()
    
    driver.quit()