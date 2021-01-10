# By Morteza Jan 3 2021
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pyautogui
import validators
import requests
import speech_recognition as sr
import re
from time import sleep
import ps
import os
import shutil
import sys
import doctest
import logging

logging.getLogger().setLevel(logging.INFO)


# Global variable
tg_desktop = '' # telegram desktop process.
browser = webdriver.Chrome(executable_path='{0}/chromedriver'.format(os.getcwd())) # Chrome driver

def CheckInput(email : str, password : str, country_code : str, phone_number : str) :
    """Check and validate input.

    >>> print(CheckInput("test@gmail.com","1234567","+1","16124219326")) # Everythin is OK
    True
    >>> print(CheckInput("testgmail.com","1234567","+1","+16124219326")) # Wrong Email
    False
    >>> print(CheckInput("test@gmail.com","1234567","+1","3823")) # Wrong Phone Number
    True
    >>> print(CheckInput("test@gmail.com","","+1","+16124219326")) # Empty Password
    False
    """
    validate_phone_pattern = r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"

    if validators.email(email) and password:
        return True
    else:
        return False

# When register be complate and user loged in
def TgMainPage():
    logging.info('Looking for Telegram main page')
    while pyautogui.locateOnScreen("img/tg_main.png", confidence=0.9) is None:
        sleep(.5)
    logging.info('User is now loggin')

def CreateTelegram(phone_number : str):
    """Create a new folder and copy telegram app to that.

    Args:
        phone_number (str): a phone number that used for foldername

    """

    basic_telegram_location= '{0}/Telegram.exe'.format(os.getcwd())
    account_dir='{0}/Accounts/'.format(os.getcwd())
    dest= '{0}{1}'.format(account_dir ,phone_number)

    if not os.path.exists(account_dir):
        os.mkdir(account_dir)

    logging.info("Create folder for new phone number")
    if not os.path.exists(dest):
        os.mkdir(dest)
    else:
        logging.info("{0} exist".format(dest))

    logging.info("Copy telegram basic to new folder")
    shutil.copy(basic_telegram_location, dest)


def RunTelegram(phone_number : str):
    """Run telegram app with wine

    Args:
        phone_number (str): phone number
    """

    tg_exe_location= 'Accounts/{phone}/Telegram.exe'.format(phone = phone_number)

    logging.info("Run telegram app with wine")
    tg_desktop = ps.start("wine {0}".format(tg_exe_location))

    logging.info("Wait 20 seconds")
    sleep(20)
    second_wait=0 # for try count of wait for load telegram

    logging.info("Detect Telegram is loading...")
    while pyautogui.locateOnScreen("img/telegram_first_screen.png", confidence=0.9) is None: # Wait until telegram app full loaded
        second_wait+=1
        sleep(1)

        if second_wait>=10: # seems that telegram not loading
            logging.warning("Start messaging button not found")
            browser.close()
            exit()

    return True

# Check when code enter for active Telegram is valid
def CheckValidCode():
    logging.info("Check that code is valid...")
    sleep(.5)
    invalid_code = pyautogui.locateOnScreen("img/invalid_code.png", confidence=0.9)
    if invalid_code is not None :
        logging.info("Activation code is invalid!")
        exit()

def ForgetPassword():
    logging.info("Check that account set password")
    sleep(.5)
    forget_password = pyautogui.locateOnScreen("img/forget_password.png", confidence=0.9)
    if forget_password is not None :
        logging.info("Account has password")
        exit()

def CheckBannedPhone():
    logging.info("Check that phone is banned")
    phone_banned = pyautogui.locateOnScreen("img/phone_banned.png", confidence=0.9) # Location of phone_banned on screen
    if phone_banned is not None:
        logging.info('Your phone is banned')
        browser.close()
        exit()


# Check that flooding number
def FloodNumber():
    logging.info("Check too many try")
    flood_number = pyautogui.locateOnScreen("img/many_try.png", confidence=0.9) # Location of phone_banned on screen
    if flood_number is not None:
        logging.info('Click on send via sms')
        browser.close()
        exit()

def SendViaSMS():
    logging.info("Look for send via sms")
    via_sms = pyautogui.locateOnScreen("img/via_sms.png", confidence=0.9) # Location of phone_banned on screen
    if via_sms is not None:
        logging.info('Click on send via sms')
        sms_btn=pyautogui.center(via_sms)
        btn_x,btn_y=sms_btn
        pyautogui.click(btn_x,btn_y)


def ControlTelegram(phone_number : str):
    """Control Telegram desktop and control it with pyautogui.
    Args:
        country_code (str): for example +1
        phone_number (str): for example 6124219326
    """

    # Control telegram desktop to register new phone with keyboard and mouse
    CreateTelegram(phone_number)

    if RunTelegram(phone_number):
        logging.info("Find Start messaging buttton on telegram app")
        start_btn = pyautogui.locateOnScreen("img/start_messaging.png", confidence=0.9) # Location of start messaging on screen
        if start_btn is not None:
            start_btn = pyautogui.center(start_btn)
            btn_x, btn_y = start_btn
            logging.info("Click on Start messaging button")
            pyautogui.click(btn_x,btn_y)

            sleep(1)

            qr_code = pyautogui.locateOnScreen("img/login_via_phone_number.png", confidence=0.9)

            if qr_code is not None:
                qr_page = pyautogui.center(qr_code)
                qr_x,qr_y = qr_page
                pyautogui.click(qr_x,qr_y)
                pyautogui.press('enter')

                sleep(.5)

        else:
            logging.warning("Start messaging button not found")
            exit()

        logging.info("Find NEXT buttton location on telegram app")
        next_btn = pyautogui.locateOnScreen("img/next_btn.png", confidence=0.9) # Location of start messaging on screen        
        if next_btn is not None:
            next_btn=pyautogui.center(next_btn)
            btn_x,btn_y=next_btn

            logging.info("Find country code location")
            pyautogui.doubleClick(btn_x-100,btn_y-90) # 100 and 90 get it in test mode. maybe need  to change it            pyautogui.press("backspace")
            pyautogui.write("+1")
            pyautogui.press("tab")
            pyautogui.write(phone_number)
            pyautogui.press('enter')
            sleep(2)
            CheckBannedPhone() # Check that the phone number is banned
            FloodNumber()
            SendViaSMS()
            logging.info("Send activation code via telegram. wait 4.30 minutes")
        else:
            logging.warning("NEXT button not found")
            exit()

        sleep(4*60+30) # wait until telegram call

def Download(address : str, account : str, fileName : str):
    if validators.url(address):        
        req = requests.get(address)

        if req.status_code == 200:
            dest_file = '{0}/Accounts/{1}/{2}'.format(os.getcwd(), account,fileName)
            logging.info("Save file on {0}/Accounts/{1}/{2}".format(os.getcwd(), account,fileName))
            with open(dest_file,'wb') as f:
                f.write(req.content)
        return True
    else:
        return False
        
def CorrectCode(text : str):
    """Correct google speech recognitation errors

    Args:
        text (str): a text that extract from voice

    Returns:
        string: currect code

    >>> print(CorrectCode("51971 again your code is 5519 Evan goodbye"))
    51971 again your code is 55197 goodbye
    """

    text = text.replace(' Evan ','7') # addad 7 dar bazi mavaghe ke entehaye code 'Evan' khande mishe
    text=text.replace(' four ','4')
    text=text.replace(' to ','2')

    return text


def ExtractCode(sound_address : str):
    """Extract activition code from voice call with speech recognition

    Args:
        sound_address (str): address of voice call file

    Returns:
        str: activition code

    >>> print(ExtractCode("sound_test.wav"))
    55197
    """
    r = sr.Recognizer()

    with sr.AudioFile(sound_address) as source:
        logging.info("Listenning voice mail")
        audio_text = r.listen(source)
        
        try:            
            # using google speech recognition
            r.adjust_for_ambient_noise(source, duration=1)
            text = r.recognize_google(audio_text)

            logging.info("Correct incorect number...")
            text=CorrectCode(text)

            logging.info('Converting audio transcripts into text ...')
            # (?<!^) for not start with \d{5}. referenced from https://stackoverflow.com/a/15669590
            code = re.search('(?<!^)\d{5}',text) # Find 5 digit number in text of voice mail
            if code:    
                logging.info("Activation code is {0}".format(code.group(0)))
            else:
                logging.info("Error in extract code from voice.wav")
                #exit()

            return code.group(0)

        
        except Exception as e:
            logging.error(str(e))

def Sign_Up(name : str, family : str):
    logging.info("Look for sign up button...")
    sign_up_btn = pyautogui.locateOnScreen("img/sign_up.png", confidence=0.9) # Location of sign up button on screen
    if sign_up_btn is not None:
        logging.info('Look for last name textbox')
        last_name_text=pyautogui.locateOnScreen('img/last_name.png',confidence=0.9) # Location of last name textbox on screen
        if last_name_text is not None:
            last_name_text = pyautogui.center(last_name_text)
            btn_x,btn_y=last_name_text
            logging.info('Click on last name textbox')
            last_name_text.click(btn_x,btn_y)
            pyautogui.write(family)
            pyautogui.press('tab')
            pyautogui.write(name)
            pyautogui.press('enter')
            logging.info("Click on SIGN UP button....")




def GenerateFakePerson(phone_number : str):
    logging.info('Open https://www.fakepersongenerator.com for generate fake person')
    browser.get('https://www.fakepersongenerator.com/Index/generate')


    logging.info("Wait until fake user image is loading...")
    WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'face')))

    avatar_location = browser.find_elements_by_class_name('img-responsive')[1]
    avatar_location = avatar_location.get_attribute('src')


    logging.info("Download {0}".format(avatar_location))
    if Download(avatar_location,phone_number,'avatar.jpg'):
        sex = avatar_location.split('/')[-2]
        name = browser.find_element_by_class_name('name')
        name = name.find_element_by_class_name('click').text
        name = name.split()[0]
        family = name.split()[-1]

        country = browser.find_elements_by_class_name('form-control')[-2]
        country = country.get_attribute('value')

        logging.info("Fake name is {0} {1}. Sex is {2}. Your country is {3}".format(name,family,sex,country))

        Sign_Up(name,family)

        dest_file = '{0}/Accounts/{1}/{2}'.format(os.getcwd(), phone_number,'info.txt')
        with open(dest_file,'w') as f:
            f.write('{0} {1}\n{2}\n{3}'.format(name,family,sex,country))
        logging.info('Create info.txt at {0}'.format(dest_file))
    else:
        logging.info('Address of voice mail is incorrect')



# After get activition code from voice mail enter it on telegram
def SubmitCodeTG(code : str):
    logging.info("Find NEXT button location")
    next_btn = pyautogui.locateOnScreen("img/next_btn.png", confidence=0.9) # Location of start messaging on screen
    if next_btn is not None:
        next_btn=pyautogui.center(next_btn)

        btn_x,btn_y=next_btn

        logging.info("Enter Activation Code")
        pyautogui.click(btn_x,btn_y-160) # 160 get it in test mode. maybe need  to change it
        pyautogui.write(code)
        pyautogui.press('enter')
        logging.info("Logging to telegram...")

        CheckValidCode() # Check that the code entered is correct

    else:
        logging.warning("NEXT button not found")
        exit()
        

def CorrectPhoneNumber(phone_number : str):
    """Remove (,),- form phone number

    Args:
        phone_number (str): phone number

    Returns:
        [string]: Correct phone number

    >>> print(CorrectPhoneNumber("(713) 681-3476"))
    7136813476
    """

    phone_number = ''.join(re.findall('\d+',phone_number))
    return phone_number


def OpenBrowser(username : str, password : str):
    logging.info("Load chrome driver")
    
    logging.info("chrome driver was loaded")
    logging.info("Open https://www.textnow.com/login")
    browser.get('https://www.textnow.com/login')

    
    while True: # Sometimes web not loading and get time out error. refresh site until full load
        try:
            logging.info("Wait 60 seconds until uikit-text-field__input is located")
            WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'uikit-text-field__input')))

            logging.info("Find txt-username")
            user_name = browser.find_element_by_id('txt-username')

            logging.info("write username")
            user_name.send_keys(username)

            logging.info("find txt-password")
            pass_elem = browser.find_element_by_id('txt-password')
            
            logging.info("write password and press enter key")
            pass_elem.send_keys(password, Keys.RETURN)
            try: # Check if password is wrong
                logging.info("Checking correct username and password")
                WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'uikit-text--danger')))
                logging.warning("Username or password is incorrect")
                browser.close()
                exit()
            except TimeoutException: # Password is OK
                logging.info("Start login...")
                break

            

        except TimeoutException:
            logging.warning("https://www.textnow.com/login not loading")
            browser.refresh()

    ref_count=0 #count of refresh that chat-preview-list not found
    while True:
        try:
            logging.info("Looking for chat-preview-list")
            WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'chat-preview-list')))
            break
        except TimeoutException:
            logging.warning("Can't locate chat-preview-list. Refresh browser..")
            browser.refresh()
            print("Can't locate chat-preview-list")
            ref_count+=1
            if ref_count>3:
                logging.warning("after 3 try, Can't find chat-preview-list and exit")
                browser.close()
                exit(1)

    phone_number=browser.find_element_by_class_name('phoneNumber').text
    logging.info("Account phone number is {0}".format(phone_number))

    phone_number=CorrectPhoneNumber(phone_number)
    account_phone_number = phone_number

    logging.info("Start Telegram Desktop...")
    ControlTelegram(phone_number) # Run telegram app


    logging.info("Refresh browser...")
    browser.refresh()

    while True:
        try:
            logging.info("Looking for chat-preview-list")
            WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'chat-preview-list')))
            break
        except TimeoutException:
            logging.info("Can't locate chat-preview-list. Refresh browser..")
            browser.refresh()
            print("Can't locate chat-preview-list")
            ref_count+=1
            if ref_count>3:
                logging.info("after 3 try, Can't find chat-preview-list and exit")
                browser.close()
                exit(1)

    logging.info("Find voice mail")
    # For Message: stale element reference: element is not attached to the page document bug. reference at https://stackoverflow.com/a/54230335
    try:
        call_sound = browser.find_elements_by_class_name('voiceMailAudio')
        address=call_sound[-1].get_attribute('src')
    except Exception as e:
        call_sound = browser.find_elements_by_class_name('voiceMailAudio')
        address=call_sound[-1].get_attribute('src')
    logging.info("Voice mail address is :{0}".format(address))

    if Download(address,phone_number,'voice.wav'):
        tg_activation_code = ExtractCode("Accounts/{0}/voice.wav".format(phone_number))
    else:
        tg_activation_code='0'
    return [tg_activation_code,phone_number]



def Main():
    doctest.testmod()
    if len(sys.argv) >= 3:
        textnow_username = sys.argv[1]
        textnow_password = sys.argv[2]

        tg_activation_code,phone_number = OpenBrowser(textnow_username,textnow_password)
        
        # disable until find a method to get 100 percent accuracy
        # SubmitCodeTG(tg_activation_code)
        ForgetPassword()
        GenerateFakePerson(phone_number)
        browser.close()
        sleep(5)
        TgMainPage()
        logging.info('Complate sign up')
        ps.terminate(tg_desktop)
    else:
        logging.error("Error in inputs")
        print("Please enter all inputs.\nemail password phone_number")
        exit()

if __name__ == "__main__":
    Main()

# Control telegram desktop to register new phone with keyboard and mouse
# pyautogui.click(730,282)
# pyautogui.moveTo(779, 517, duration = 1)
# pyautogui.click(779, 517)
# pyautogui.moveTo(997, 554, duration = 1)
# pyautogui.click(997, 554)
# pyautogui.doubleClick(997,554)
# pyautogui.press('backspace')
# pyautogui.write("+1")
# pyautogui.press('tab')
# pyautogui.write("6124219326")
# pyautogui.press('enter')

# sleep(4*60) # wait until telegram call

# Start telegram cli
# profile_path='/home/morteza/.telegram-cli/profile_7'
# if os.path.isdir(profile_path):
#     shutil.rmtree(profile_path)
# tg_cli = ps.start("telegram-cli -p profile_7 -k tg-server.pub -W")
# keel_log = ps.start("bash keep_log.sh")

# sleep(10)
# ps.write(tg_cli, "+19167446972")
# sleep(10) # Wait for recieve code in telegram

# with open('notif.log','r') as f:
#     notif=f.readline()
#     print(notif)
#     code=re.search("(Login code: )\d{5}",notif)
#     code=re.search("\d{5}",code[0])
# print("code is :",code[0])
# ps.write(tg_cli,code[0])
# ps.terminate(keel_log)
# os.remove('notif.log')



    


# browser = webdriver.Chrome(executable_path='chromedriver')
# browser.get('https://www.textnow.com/login')

# try:
#     WebDriverWait(browser,30).until(EC.presence_of_element_located((By.CLASS_NAME, 'uikit-text-field__input')))
#     print("Find uikit-text-field__input")
#     user_name = browser.find_element_by_id('txt-username')
#     print("Find txt-username")
#     user_name.send_keys("mortezasaki91@gmail.com")
#     password = browser.find_element_by_id('txt-password')
#     print("Find txt-password")
#     password.send_keys("6881977858",Keys.RETURN)

#     try:
#         WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'chat-preview-list')))
#         call_sound = browser.find_elements_by_class_name('voiceMailAudio')
#         address=call_sound[-1].get_attribute('src')
#         print(address)
#         req = requests.get(address)

#         if req.status_code == 200:
#             with open('sound.wav','wb') as f:
#                 f.write(req.content)
            
#             r = sr.Recognizer()


#         with sr.AudioFile('./sound.wav') as source:
            
#             audio_text = r.listen(source)
            
#             try:
                
#                 # using google speech recognition
#                 text = r.recognize_google(audio_text)
#                 text = text.replace(' Evan','7') # addad 7 dar bazi mavaghe ke entehaye code 'Evan' khande mishe
#                 print('Converting audio transcripts into text ...')
#                 print(text)
#                 code = re.search('\d{5,}',text) # Peida kardan code 5 raghami dar tamas
                    
#                 print(code[0])

#                 ps.write(process,code[0]) # Input Activation Code

#                 # pyautogui.moveTo(1010, 478, duration = 1)
#                 # pyautogui.write(code[0]) # Enter code in telegram for signup
#                 # pyautogui.press('enter')

            
#             except Exception as e:
#                 print(str(e))
#     except:
#         print("error in chat-preview-list")

# except:
#     print("error in loadning txt-username")

# input("Press enter to close")
# ps.terminate(tg_cli)
# browser.close()

