from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import pytest

def test_Sauce_title():
    # Inicializa el WebDriver para Chrome
    driver = webdriver.Chrome()
    
    # Navega al URL de la aplicación que queremos testear.
    driver.get("https://www.saucedemo.com/")

    # Testear si el titulo es correcto
    assert "Swag Labs" in driver.title

    # Cerrar the driver
    driver.quit()

# Ejercicio 2 - Login
def test_Sauce_login():
    # Inicializa el WebDriver para Chrome
    driver = webdriver.Chrome()
    
    # Navega al URL de la aplicación que queremos testear.
    driver.get("https://www.saucedemo.com/")
    sleep(3)

    # Localizar username y escibir uno
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    
    # Localizar password y escibir uno
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    
    # Localizar el botón y hacer click
    driver.find_element(By.ID, "login-button").click()
    sleep(5)
    
    text = driver.find_element(By.CLASS_NAME, "title").text
    
    # Verificar si el login ha ido correcto, mirando si hemos cambiado de pagina
    assert "products" in text.lower()
    
    # Cerrar the driver
    driver.quit()
    
# Ejercicio 3 - Logout
def test_Sauce_logout():
    # Inicializa el WebDriver para Chrome
    driver = webdriver.Chrome()
    
    # Navega al URL de la aplicación que queremos testear.
    driver.get("https://www.saucedemo.com/")
    
    #Hacer el login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Localizar el menu, haz click para abrirlo
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    sleep(3)
    
    # Localizar logout y hacer click
    driver.find_element(By.ID, "logout_sidebar_link").click()
    
    # Check we are back at the login page
    inputs = driver.find_elements(By.TAG_NAME, "input")
    assert len(inputs) == 3
    for i in inputs:
        assert (i.get_attribute("name")) in ["user-name", "password", "login-button"]
    
    # Cerrar the driver
    driver.quit()
    
    

# Ejercicio 4 - Añadir producto al carrito y verificar que esta
# test que añade un producto al carito de compras y verifica que el producto esta ahi despues
def test_add_to_cart():
    # Inicializa el WebDriver para Chrome
    driver = webdriver.Chrome()
    
    # Navega al URL de la aplicación que queremos testear.
    driver.get("https://www.saucedemo.com/")
    
    # Hacer el login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    sleep(2)
    
    # Obtener el nombre del primer producto para verificar después
    product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    
    # Añadir el producto al carrito
    driver.find_element(By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']").click()
    sleep(1)
    
    # Verificar que el contador del carrito muestre 1
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1"
    
    # Navegar al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    sleep(2)
    
    # Verificar que el producto está en el carrito
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 1
    
    # Verificar que el producto en el carrito es el mismo que añadimos
    cart_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert cart_product_name == product_name
    
    # Cerrar the driver
    driver.quit()
