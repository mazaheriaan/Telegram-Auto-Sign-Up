from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import logging
import utility

logger = logging.getLogger()
logger.level = logging.INFO
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
            WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'uikit-text--danger')))
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
            user_elem = self.browser.find_element_by_id('txt-username')

            logging.info("write username")
            user_elem.send_keys(user_name)

            logging.info("find txt-password")
            pass_elem = self.browser.find_element_by_id('txt-password')
        
            logging.info("write password and press enter key")
            pass_elem.send_keys(password, Keys.RETURN)

            if self.__incurrect_account():
                return False
            else:
                return True

        except TimeoutException:
            logging.warning("https://www.textnow.com/login not loading")
            self.browser.refresh()
            return False

    def AreaCode(self):
        try:
            logging.info("Checking for area code input")
            WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.ID, 'enterAreaCodeForm')))
            area_code_form = self.browser.find_element_by_id('enterAreaCodeForm')
            txt = area_code_form.find_element_by_css_selector('#enterAreaCodeForm > div.content > input[type=text]')
            txt.send_keys('912', Keys.RETURN)
        except TimeoutException:
            logging.info('Area code input not found.')

    def TermAccept(self):
        try:
            logging.info("Accept 911 term of service")
            WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.ID, 'iAgree')))
            agree = self.browser.find_element_by_id('iAgree')
            agree.click()
        except:
            logging.info('Accept button not found')


    def ExtractPhoneNumber(self):
        try:
            logging.info("Looking for phoneNumber")
            WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'phoneNumber ')))
            self.phone_number = self.browser.find_element_by_class_name('phoneNumber').text
            logging.info("Account phone number is {0}".format(self.phone_number))
            self.phone_number = utility.RemoveParenthesisFromPhone(self.phone_number)
            return self.phone_number
        except TimeoutException:
            logging.warning("Can't locate phoneNumber. Refresh browser..")
            return None

    def FindTelegramVoiceCall(self):
        try:
            logging.info('Looking for Telegram message...')
            list_cell = self.browser.find_elements_by_class_name('uikit-summary-list__cell-content--fill')
            if len(list_cell) > 0:
                for l in list_cell:
                    message = l.find_elements_by_tag_name('span')
                    print(message)
                    if 'voicemail' in message[1].text or 'Voicemail' in message[1].text or message[0].text == '(213) 320-2789':
                        logging.info('Click on telegram message for loading messages')
                        l.click()
                        return True
                return False
            else:
                logging.info("Can't find Telegram message")
                return False
        except NoSuchElementException:
            logging.info("Can't find Telegram message")
            return False


    
    def DownloadVoiceMail(self):
        try:
            logging.info("Looking for voiceMailAudio")
            WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'voiceMailAudio')))
            try:
                call_sound = self.browser.find_elements_by_class_name('voiceMailAudio')
                address=call_sound[-1].get_attribute('src') # Last voice mail
            except Exception as e:
                call_sound = self.browser.find_elements_by_class_name('voiceMailAudio')
                address = call_sound[-1].get_attribute('src')

            logging.info("Voice mail address is :{0}".format(address))
            logging.info("Start download voice mail...")
            dest = 'Accounts/{0}/voice.wav'.format(self.phone_number)
            if utility.DownloadFile(address, dest):
                logging.info("Voice mail download is complated!")
                return dest
            else:
                logging.info("Voice mail download is fail!")
                return None
        except:
            logging.error('Error in DownloadVoiceMail')

    def Close(self):
        self.browser.close()

    def GetPhoneNumber(self):
        if self.phone_number != '':
            return self.phone_number
        return None