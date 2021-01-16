from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
import utility


class FakePerson:
    def __init__(self, location, sex):
        logging.info("Load chrome driver")
        self.browser = webdriver.Chrome(executable_path='./chromedriver') # Chrome driver
        logging.info("chrome driver was loaded")

        logging.info('Open https://www.fakepersongenerator.com for generate fake person')
        self.browser.get('https://www.fakepersongenerator.com/Index/generate')

    def GetName(self):
        name = self.browser.find_element_by_class_name('name')
        return name

    def GetCountry(self):
        country = self.browser.find_elements_by_class_name('form-control')[-2]
        country = country.get_attribute('value')
        return country

    def DownloadImage(self, dest : str):
        logging.info("Wait until fake user image is loading...")
        WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'face')))
        avatar_location = self.browser.find_elements_by_class_name('img-responsive')[1]
        avatar_location = avatar_location.get_attribute('src')
        
        logging.info("Download {0}".format(avatar_location))
        if utility.DownloadFile(avatar_location, dest, 'avatar.jpg'):
            return avatar_location
        
        return None

    def Generate(self, dest : str):
        avatar_location = DownloadImage(dest)

        if avatar_location is not None:
            sex = avatar_location.split('/')[-2]
            name = GetName()
            family = name.split()[-1]
            name = name.split()[0]
            country = GetCountry()

            return [avatar_location, name, family, sex, country]
        else:
            return False
