from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
import utility

class TextNow:

    def __init__(self):
        self.phone_number = ''
        logging.info("Load chrome driver")
        self.browser = webdriver.Chrome(executable_path='./chromedriver') # Chrome driver
        logging.info("chrome driver was loaded")

        logging.info("Open https://www.textnow.com/login")
        self.browser.get('https://www.textnow.com/login')

    def __incurrect_account(self): # Check that username or password is currect and succesful login
        try: # Check if password is wrong
            logging.info("Checking correct username and password")
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'uikit-text--danger')))
            logging.error("Username or password is incorrect")
            return True # Account is not currect
        except TimeoutException: # Password is OK
            logging.info("Start login...")
            return False # Account is currect
    
    def Login(self, user_name : str, password : str):
    
        try:
            logging.info("Wait 60 seconds until uikit-text-field__input is located")
            WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'uikit-text-field__input')))

            logging.info("Find txt-username")
            user_name = self.browser.find_element_by_id('txt-username')

            logging.info("write username")
            user_name.send_keys(user_name)

            logging.info("find txt-password")
            pass_elem = self.browser.find_element_by_id('txt-password')
        
            logging.info("write password and press enter key")
            pass_elem.send_keys(password, Keys.RETURN)

            if utility.RepeatFunc( self.__incurrect_account()):
                return False
            else:
                return True

        except TimeoutException:
            logging.warning("https://www.textnow.com/login not loading")
            self.browser.refresh()
            return False

    #def PhoneNumber():

    def GetPhoneNumber(self):
        try:
            logging.info("Looking for phoneNumber")
            WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'phoneNumber ')))
            self.phone_number = self.browser.find_element_by_class_name('phoneNumber').text
            logging.info("Account phone number is {0}".format(self.phone_number))
            return True
        except TimeoutException:
            logging.warning("Can't locate phoneNumber. Refresh browser..")
            return False

    def DownloadVoiceMail(self):
        try:
            logging.info("Looking for voiceMailAudio")
            WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'voiceMailAudio')))
            try:
                call_sound = browser.find_elements_by_class_name('voiceMailAudio')
                address=call_sound[-1].get_attribute('src') # Last voice mail
            except Exception as e:
                call_sound = self.browser.find_elements_by_class_name('voiceMailAudio')
                address = call_sound[-1].get_attribute('src')

            logging.info("Voice mail address is :{0}".format(address))
            logging.info("Start download voice mail...")
            if utility.DownloadFile(address, self.phone_number, 'voice.wav'):
                logging.info("Voice mail download is complated!")
                return True
            else:
                logging.info("Voice mail download is fail!")
                return False
        except:
            print("Error")

    def Close(self):
        self.browser.close()