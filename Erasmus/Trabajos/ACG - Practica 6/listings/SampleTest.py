import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

def test_lambdatest_todo_app():
    
    # Inicializa el WebDriver para Chrome
    chrome_driver = webdriver.Chrome()
    
    # Navega al URL de la aplicación que queremos testear.
    chrome_driver.get('https://lambdatest.github.io/sample-todo-app/')
    
    # Maximiza la ventana del navegador para asegurar que todos los 
    # elementos de la página sean visibles.
    chrome_driver.maximize_window()
    
    # Los siguientes dos comandos encuentran elementos en la página web
    # con el metodo find_element. Los ejemplos usan el atributo 'name'
    # para encontrarlos y realizan un click() en ellos.
    # Podemos usar la función de herramienta de inspección del navegador Chrome
    # para inspeccionar los detalles de los elementos web requeridos.
    
    chrome_driver.find_element(By.NAME,"li1").click()
    chrome_driver.find_element(By.NAME,"li2").click()
    
    #Verificar el titulo de la pagina
    assert chrome_driver.title == "Sample page - lambdatest.com"
    
    # Encontrar el textfield para añadir un todo
    todo_text_field = chrome_driver.find_element(By.ID, "sampletodotext")
    
    # Escri¡bir un texto ahi
    sample_text = "Happy Testing at LambdaTest"
    todo_text_field.send_keys(sample_text)

    
    # Haz click en el b¡utton add
    chrome_driver.find_element(By.ID,"addbutton").click()  
    
    #ahora tiene que haber un sexto elemento
    chrome_driver.find_element(By.NAME,"li6").click()
       
    # Extraer y verificar que el texto asociado al 'li6' sea "sample_text"
    # Asumiendo que el texto está en un <span> justo al lado del input del checkbox
    li6_span_text = chrome_driver.find_element(By.XPATH,
                                               '//input[@name="li6"]/following-sibling::span'
                                               ).text
    assert li6_span_text == sample_text, "El texto asociado al li6 no es el esperado"
    
    chrome_driver.close()