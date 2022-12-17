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

class HomepageTestCase(BaseTestCase):
    
    def setUp(self):
        self.base = BaseTestCase()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        super().setUp() 
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()
    
    def test_get_homepage(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState= self.driver.find_element(By.TAG_NAME,"h1").text
        self.assertTrue(vState, "Voting in Decide")
    
    def test_get_contenedor(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState= self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Redirección de modulos")  
    
    def test_redireccion_Admin(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "Administrador")
        vState.click() 
        assert self.driver.find_element(By.LINK_TEXT, "Django administration").text == "Django administration"
    
    def test_redireccion_Doc(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "Doc")
        vState.click() 
        assert self.driver.find_element(By.TAG_NAME,"h2").text == "Decide API"
    
    def test_redireccion_Authentication(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "authentication")
        vState.click() 
        assert self.driver.find_element(By.LINK_TEXT, "Django administration").text == "Django administration"
    
    def test_redireccion_Base(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "Base")
        vState.click() 
        assert self.driver.find_element(By.LINK_TEXT, "Django administration").text == "Django administration"
    
    def test_redireccion_Census(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "Census")
        vState.click() 
        assert self.driver.find_element(By.LINK_TEXT, "Django administration").text == "Django administration" 
    
    def test_redireccion_Postproc(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "Postproc")
        vState.click() 
        assert self.driver.find_element(By.TAG_NAME,"h1").text == "Post Proc"
    
    def test_redireccion_Voting(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState = self.driver.find_element(By.LINK_TEXT, "Voting")
        vState.click() 
        assert self.driver.find_element(By.LINK_TEXT, "Django administration").text == "Django administration" 
    
    def test_get_Votings(self):
        self.driver.get("http://127.0.0.1:8000/")
        vState= self.driver.find_element(By.TAG_NAME,"h2").text
        self.assertTrue(vState, "Votings")  
    
    
 
    
        
  

    
  
