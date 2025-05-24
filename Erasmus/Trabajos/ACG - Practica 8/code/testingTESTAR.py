from TESTAR_template import testar, start_SUT_and_get_driver
from selenium.webdriver.common.by import By
import os


def test_lambda():
    
    testar('https://lambdatest.github.io/sample-todo-app/', 3, 5, [], [])


def test_saucer():
  
    def test_Sauce_login(driver):
       
        # Localizar username y escibir uno
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        
        # Localizar password y escibir uno
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        
        # Localizar el botón y hacer click
        driver.find_element(By.ID, "login-button").click()
        
    def filter_burger(driver):
        return driver.find_element(By.ID, "react-burger-menu-btn")
    
    def filter_external_links(driver):
        all_links = driver.find_elements(By.TAG_NAME, "a")
        
        # Filter the links to Twitter, Facebook and LinkedIn
        social_links = [ link for link in all_links if link.get_attribute("href") and any(social in link.get_attribute("href") for social in ["twitter.com", "facebook.com", "linkedin.com"])]
        
        return social_links
    
    def filter_elements_with_accessibility_issues(driver):
        # Apparently not needed no more
        return []
    
    # Combine all filters
    all_filters = [filter_burger, filter_external_links, filter_elements_with_accessibility_issues]
    
    # Run test with all filters and skip_accessibility=True
    testar("https://www.saucedemo.com/", 1, 20, all_filters, [test_Sauce_login], skip_accessibility=True)
     
    

def test_practicesoftwaretesting():
    # Run with fewer actions and skipping both accessibility and image checks
    testar("https://v1.practicesoftwaretesting.com/#/", 1, 20, [], [], 
           skip_accessibility=True, skip_image_check=True)


if __name__ == "__main__":
    print("Running Lambda Test")
    test_lambda()
    
    print("\nRunning Sauce Demo Test")
    test_saucer()
    
    print("\nRunning Practice Software Testing")
    test_practicesoftwaretesting()
    
    print("\nAll tests completed.")

