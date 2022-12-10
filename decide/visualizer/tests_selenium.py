from base.tests import BaseTestCase
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestSeleniumVisualizer(BaseTestCase):
    
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
  
    def teardown_method(self, method):
        self.driver.quit()  

    
    def teardown_method(self, method):
        self.driver.quit()
    
    def test_testaccessvisualizer200(self):
        self.driver = webdriver.Chrome()
        response = self.driver.get("http://localhost:8000/visualizer/6/")
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"

    def test_untitled(self):
        self.driver = webdriver.Chrome()
        response = self.driver.get("http://localhost:8000/visualizer/6/")
        self.driver.find_element(By.CSS_SELECTOR, "span:nth-child(1)").click()
        '''
        assert self.driver.find_element(By.CSS_SELECTOR, ".text-muted > th:nth-child(1)").text == "Opción"
        assert self.driver.find_element(By.CSS_SELECTOR, "th:nth-child(2)").text == "Puntuación"
        assert self.driver.find_element(By.CSS_SELECTOR, "th:nth-child(3)").text == "Votos"
        '''
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"
    
    def test_lightmode(self):
        self.driver = webdriver.Chrome()
        response = self.driver.get("http://localhost:8000/visualizer/6")
        self.driver.find_element(By.CSS_SELECTOR, "span:nth-child(1)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"
        self.driver.find_element(By.CSS_SELECTOR, "span:nth-child(2)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Votación no comenzada"
  
    
  
    
    


    