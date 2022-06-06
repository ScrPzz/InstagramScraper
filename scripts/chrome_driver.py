from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from time import sleep
import urllib.parse
from collections import namedtuple
from browsermobproxy import Server


class ChromeDriver:
    def __init__(self):
        pass

    def set_up_proxy(self):
        server = Server("./bin/browsermob-proxy-2.1.4/bin/browsermob-proxy")
        server.start()
        proxy=server.create_proxy()
        return proxy


    def set_up_driver(self, proxy):
        #proxy=self.set_up_proxy() 

        co = webdriver.ChromeOptions()
        co.add_argument('--ignore-ssl-errors=yes')
        co.add_argument('--ignore-certificate-errors')
        if proxy:
            co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=proxy.port))
        #co.add_argument("--incognito")
        #co.add_argument("--disable-notifications")
        #co.add_argument("--disable-extensions") 
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=co)

        return driver

    def make_IG_access(self, driver, ig_usr, ig_pass, **kwargs):

        driver.get('https://www.instagram.com/')
        wait = WebDriverWait(driver, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]'))) # Bypass cookies wall

        driver.find_element(by=By.XPATH, value='//input[@name="username"]').send_keys(ig_usr)
        driver.find_element(by=By.XPATH, value='//input[@type="password"]').send_keys(ig_pass)
        driver.find_element(by=By.XPATH, value='//input[@type="password"]').submit() 

        if 'steps' in kwargs.keys():
            for step in range(0, int(kwargs['steps'])):
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click() # Do not save login infos 
                wait = WebDriverWait(driver, 30)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click() # Disable notifications 
                wait = WebDriverWait(driver, 30)
        else:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click() # Do not save login infos 
            wait = WebDriverWait(driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))).click() # Disable notifications 
            wait = WebDriverWait(driver, 30)
        return driver