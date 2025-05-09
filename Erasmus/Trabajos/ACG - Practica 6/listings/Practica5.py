
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import pytest


def test_contact_form_submission():
   # Inicializa el WebDriver para Chrome
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   # Acceder al formulario
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)   # Rellenar formulario
   driver.find_element(By.ID, "first_name").send_keys("Alice")
   driver.find_element(By.ID, "last_name").send_keys("Smith")
   driver.find_element(By.ID, "email").send_keys("alice@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
   driver.find_element(By.ID, "message").send_keys(6*"Hola hola!") # 60 caracteres
   # Enviar
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   # Verificar mensaje de éxito
   success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
   assert "Thanks for your message" in success_msg
   # Cerrar the driver
   driver.quit()

# Caso positivo 2: Usar diferente valor válido para el dropdown "Subject"
def test_contact_form_different_subject():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)   
   driver.find_element(By.ID, "first_name").send_keys("Bob")
   driver.find_element(By.ID, "last_name").send_keys("Johnson")
   driver.find_element(By.ID, "email").send_keys("bob@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Webmaster")
   driver.find_element(By.ID, "message").send_keys("Este mensaje tiene más de 50 caracteres como es requerido por el formulario de contacto.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
   assert "Thanks for your message" in success_msg
   
   driver.quit()

# Caso positivo 3: Usar un mensaje muy largo
def test_contact_form_long_message():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)   
   driver.find_element(By.ID, "first_name").send_keys("Charlie")
   driver.find_element(By.ID, "last_name").send_keys("Brown")
   driver.find_element(By.ID, "email").send_keys("charlie@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Return")
   driver.find_element(By.ID, "message").send_keys("A" * 200)  # 200 caracteres
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
   assert "Thanks for your message" in success_msg
   
   driver.quit()

# Caso positivo 4: Usar caracteres especiales en los campos de nombre
def test_contact_form_special_chars():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   driver.find_element(By.ID, "first_name").send_keys("María-José")
   driver.find_element(By.ID, "last_name").send_keys("Rodríguez O'Hara")
   driver.find_element(By.ID, "email").send_keys("maria.jose@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Payments")
   driver.find_element(By.ID, "message").send_keys("Este mensaje contiene caracteres especiales: áéíóú ñ çã. Y tiene más de 50 caracteres.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
   assert "Thanks for your message" in success_msg
   
   driver.quit()

# Caso positivo 5: Usar una dirección de email compleja pero válida
def test_contact_form_complex_email():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   driver.find_element(By.ID, "first_name").send_keys("David")
   driver.find_element(By.ID, "last_name").send_keys("Wilson")
   driver.find_element(By.ID, "email").send_keys("david.wilson+test123@sub.example-domain.co.uk")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
   driver.find_element(By.ID, "message").send_keys("Este es un mensaje de prueba que tiene más de cincuenta caracteres como se requiere.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
   assert "Thanks for your message" in success_msg
   
   driver.quit()

# Caso negativo 1: Campo de nombre faltante
def test_contact_form_missing_first_name():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   # No se introduce el nombre
   driver.find_element(By.ID, "last_name").send_keys("Smith")
   driver.find_element(By.ID, "email").send_keys("test@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
   driver.find_element(By.ID, "message").send_keys("Este mensaje tiene más de 50 caracteres como es requerido por el formulario.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   # Verificar mensaje de error
   error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
   assert "required" in error_msg.lower()
   
   driver.quit()

# Caso negativo 2: Email inválido
def test_contact_form_invalid_email():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   driver.find_element(By.ID, "first_name").send_keys("John")
   driver.find_element(By.ID, "last_name").send_keys("Doe")
   driver.find_element(By.ID, "email").send_keys("john@") # Email inválido
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
   driver.find_element(By.ID, "message").send_keys("Este mensaje tiene más de 50 caracteres como es requerido por el formulario.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   # Verificar mensaje de error
   error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
   assert "valid email" in error_msg.lower()
   
   driver.quit()

# Caso negativo 3: Mensaje con menos de 50 caracteres
def test_contact_form_short_message():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   driver.find_element(By.ID, "first_name").send_keys("Emma")
   driver.find_element(By.ID, "last_name").send_keys("Garcia")
   driver.find_element(By.ID, "email").send_keys("emma@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
   driver.find_element(By.ID, "message").send_keys("Mensaje corto.") # Menos de 50 caracteres
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   # Verificar mensaje de error
   error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
   assert "50" in error_msg
   
   driver.quit()

# Caso negativo 4: Sin selección de asunto
def test_contact_form_no_subject():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   driver.find_element(By.ID, "first_name").send_keys("Frank")
   driver.find_element(By.ID, "last_name").send_keys("Miller")
   driver.find_element(By.ID, "email").send_keys("frank@example.com")
   # No se selecciona el asunto
   driver.find_element(By.ID, "message").send_keys("Este mensaje tiene más de 50 caracteres como es requerido por el formulario de contacto.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   # Verificar mensaje de error
   error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
   assert "subject" in error_msg.lower()
   
   driver.quit()

# Caso negativo 5: Apellido faltante
def test_contact_form_missing_last_name():
   driver = webdriver.Chrome()
   driver.get("https://practicesoftwaretesting.com")
   driver.find_element(By.LINK_TEXT, "Contact").click()
   sleep(1)
   
   driver.find_element(By.ID, "first_name").send_keys("Grace")
   # No se introduce el apellido
   driver.find_element(By.ID, "email").send_keys("grace@example.com")
   Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
   driver.find_element(By.ID, "message").send_keys("Este mensaje tiene más de 50 caracteres como es requerido por el formulario.")
   
   driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
   sleep(1)   # Esperar a que se procese el envío
   # Verificar mensaje de error
   error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
   assert "required" in error_msg.lower()
   
   driver.quit()