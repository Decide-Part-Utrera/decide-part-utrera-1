import random
from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from django.db import transaction

from voting.models import Voting, Question, QuestionOption
from mixnet.models import Auth
from django.contrib.auth.models import User
from base import mods
from base.tests import BaseTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import time
import json

class HomepageTestCase(BaseTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
        super().setUp()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

'''
    def test_get_homepage(self):
        self.driver.get("http://localhost:8000/")
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Voting in Decide"
    
    def test_voting(self):
        self.driver.get("http://localhost:8000/")
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".litavotings")
        assert len(elements) > 0

    def test_link_voting(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.LINK_TEXT, "Esta va").click()
        url = self.driver.current_url
        assert url == "http://localhost:8000/voting/1/"

    def tes_redirectAdmin(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/")
        elements = self.driver.find_element(By.CSS_SELECTOR, ".filas:nth-child(1) > .enlace")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.LINK_TEXT, "admin/")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.LINK_TEXT, "admin/").click()
        self.driver.find_element(By.ID, "content").click()
        self.driver.find_element(By.ID, "id_username").send_keys("carmen")
        self.driver.find_element(By.ID, "id_password").send_keys("pastrana")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        assert self.driver.find_element(By.LINK_TEXT, "Administración de Django").text == "Administración de Django"
        assert self.driver.find_element(By.CSS_SELECTOR, "strong").text == "ADMIN"
'''
       