'''

Ejemplos de casos de prueba:
[Negativo] Se intenta subir un archivo .pdf vacio Aparece un error de tipo
[Negativo] Se intenta subir un archivo .pdf de 100KB  Aparece un error de tamaño
[Negativo] Se intenta subir un archivo .txt de 100KB  Aparece un error de tamaño
[Positivo] Se sube un archivo .txt vacío (0 KB) y se envía correctamente.
Después, automatiza estos casos de prueba utilizando Selenium y pytest.
'''

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import pytest
import os

# Simulamos las rutas a archivos para pruebas (estos serían archivos reales en un entorno de pruebas)
FILE_PDF_120KB = "C:/Users/franc/OneDrive - University of Pisa/Documents/UniPi/UPV/ACG/practica67/test_files/sunflower.pdf"
FILE_TXT_EMPTY = "C:/Users/franc/OneDrive - University of Pisa/Documents/UniPi/UPV/ACG/practica67/test_files/vacio.txt"
FILE_TXT_100KB = "C:/Users/franc/OneDrive - University of Pisa/Documents/UniPi/UPV/ACG/practica67/test_files/lorem.txt"
FILE_PDF_EMPTY = "C:/Users/franc/OneDrive - University of Pisa/Documents/UniPi/UPV/ACG/practica67/test_files/vacio.pdf"

def fill_contact_form(driver, file_path=None):
    """Función auxiliar para rellenar formulario de contacto"""
    driver.find_element(By.ID, "first_name").send_keys("Test")
    driver.find_element(By.ID, "last_name").send_keys("User")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    Select(driver.find_element(By.ID, "subject")).select_by_visible_text("Customer service")
    driver.find_element(By.ID, "message").send_keys(
        "Este mensaje tiene más de 50 caracteres como es requerido por el formulario de contacto."
    )
    
    if file_path:
        # Suponemos que el elemento para subir archivos tiene un ID "file_upload"
        driver.find_element(By.ID, "attachment").send_keys(file_path)

# Caso positivo: Se sube un archivo .txt vacío (0 KB) y se envía correctamente
def test_upload_empty_txt_file():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com")
    
    # Acceder al formulario
    driver.find_element(By.LINK_TEXT, "Contact").click()
    sleep(1)
    
    # Rellenar formulario y subir archivo
    fill_contact_form(driver, FILE_TXT_EMPTY)
    
    # Enviar el formulario
    driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
    sleep(1)
    
    # Verificar mensaje de éxito
    success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Thanks for your message" in success_msg
    
    driver.quit()

# Caso negativo: Se sube un archivo .pdf de 100kb (no es vacio y el tipo no es permitido)
def test_upload_invalid_file_size_pdf():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com")
    
    # Acceder al formulario
    driver.find_element(By.LINK_TEXT, "Contact").click()
    sleep(1)
    
    # Rellenar formulario y subir archivo
    fill_contact_form(driver, FILE_PDF_120KB)
    
    # Enviar el formulario
    driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
    sleep(1)
    
    # Verificar mensaje de error
    error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "file should be empty" in error_msg.lower()
    
    driver.quit()

# Caso negativo: Se sube un archivo .txt de 100KB (no es vacio)
def test_upload_invalid_file_size_txt():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com")
    
    # Acceder al formulario
    driver.find_element(By.LINK_TEXT, "Contact").click()
    sleep(1)
    
    # Rellenar formulario y subir archivo
    fill_contact_form(driver, FILE_TXT_100KB)
    
    # Enviar el formulario
    driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
    sleep(1)
    
    # Verificar mensaje de error
    error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "file should be empty" in error_msg.lower()
    
    driver.quit()


# Caso negativo: Se sube un archivo .pdf vacio (tipo no permitido)
def test_upload_invalid_file_type_pdf():
    driver = webdriver.Chrome()
    driver.get("https://practicesoftwaretesting.com")
    
    # Acceder al formulario
    driver.find_element(By.LINK_TEXT, "Contact").click()
    sleep(1)
    
    # Rellenar formulario y subir archivo
    fill_contact_form(driver, FILE_PDF_EMPTY)
    
    # Enviar el formulario
    driver.find_element(By.XPATH, '//input[@data-test="contact-submit"]').click()
    sleep(1)
    
    # Verificar mensaje de error
    error_msg = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "file should have a txt extension" in error_msg.lower()
    
    driver.quit()
