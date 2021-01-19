import pyautogui
import utility
import shutil
import logging
import ps
import os
from time import sleep

class TelegramDesktop:

    def __init__(self, phone_number : str):
        self.phone_number = phone_number
        self.tg_desktop = '' # telegram desktop process.

        if self.__make() and self.__run():
            logging.info('Start Telegram desktop...')

    def __make(self):
        try:
            basic_telegram_location= '{0}/Telegram.exe'.format(os.getcwd())
            account_dir='{0}/Accounts/'.format(os.getcwd())
            dest= '{0}{1}'.format(account_dir, self.phone_number)

            utility.CreateDirectory(account_dir)

            logging.info("Create folder for new phone number")
            utility.CreateDirectory(dest)

            logging.info("Copy telegram basic to new folder")
            shutil.copy(basic_telegram_location, dest)
            return True
        except Exception as e:
            logging.error(str(e))
            return False

    def __run(self):
        try:
            tg_exe_location= 'Accounts/{phone}/Telegram.exe'.format(phone = self.phone_number)

            logging.info("Run Telegram desktop with wine")
            tg_desktop = ps.start("wine {0}".format(tg_exe_location))
            return True
        except Exception as e:
            logging.error(str(e))
            return False

    def __click(self, btn):
        if btn is not None:
            btn = pyautogui.center(btn)
            btn_x, btn_y = btn
            pyautogui.click(btn_x,btn_y)
            return True
        return False

    def __see(self):
        first_screen = pyautogui.locateOnScreen("img/telegram_first_screen.png", confidence=0.9)
        if first_screen is not None:
            return True
        return False # not Found Telegram first screen


    def __start(self):
        start_btn = pyautogui.locateOnScreen("img/start_messaging.png", confidence=0.9) # Location of start messaging on screen
        if self.__click(start_btn):
            logging.info("Click on Start messaging button")
            return True
        
        return False

    def __qr_screen(self):
        qr_code = pyautogui.locateOnScreen("img/login_via_phone_number.png", confidence=0.9)
        if self.__click(qr_code):
            return True
        return False

    def __banned(self):
        logging.info("Check that phone is banned")
        phone_banned = pyautogui.locateOnScreen("img/phone_banned.png", confidence=0.9) # Location of phone_banned on screen
        if phone_banned is not None:
            return True
        return False

    # Check that flooding number
    def __flood(self):
        logging.info("Check too many try")
        flood_number = pyautogui.locateOnScreen("img/many_try.png", confidence=0.9) # Location of phone_banned on screen
        if flood_number is not None:
            return True
        return False

    def __send_via_sms(self):
        logging.info("Look for send via sms")
        via_sms = pyautogui.locateOnScreen("img/via_sms.png", confidence=0.9) # Location of phone_banned on screen
        if via_sms is not None:
            self.__click(via_sms)
            return True
        return False

    # Check when code enter for active Telegram is valid
    def __check_valid_code(self):
        logging.info("Check that code is valid...")
        invalid_code = pyautogui.locateOnScreen("img/invalid_code.png", confidence=0.9)
        if invalid_code is not None :
            logging.info("Activation code is invalid!")
            exit()

    def __submit_phone_number(self):   
        logging.info("Find NEXT buttton location on telegram app")
        next_btn = pyautogui.locateOnScreen("img/next_btn.png", confidence=0.9) # Location of start messaging on screen        
        if next_btn is not None:
            next_btn=pyautogui.center(next_btn)
            btn_x,btn_y=next_btn

            logging.info("Find country code location")
            pyautogui.doubleClick(btn_x-110,btn_y-90) # 100 and 90 get it in test mode. maybe need  to change it            pyautogui.press("backspace")
            pyautogui.write("1")
            pyautogui.press("tab")
            pyautogui.write(self.phone_number)
            pyautogui.press('enter')
            return True
            
        else:
            return False

    def Forget_password(self):
        logging.info("Check that account set password")
        forget_password = pyautogui.locateOnScreen("img/forget_password.png", confidence=0.9)
        if forget_password is not None :
            logging.info("Account has password")
            self.__click(forget_password)
            while True:
                ok_btn = pyautogui.locateOnScreen("img/ok_btn.png", confidence=0.9)
                if ok_btn is not None:
                    self.__click(ok_btn)
                    while True:
                        reset_account = pyautogui.locateOnScreen("img/reset_account.png", confidence=0.9)
                        if reset_account is not None:
                            self.__click(reset_account)
                            while True:
                                reset = pyautogui.locateOnScreen("img/reset.png", confidence=0.9)
                                if reset is not None:
                                    self.__click(reset)
                                    sleep(2)
                                    return True
                                else:
                                    logging.error('img/reset.png not found')
                                    sleep(1)
                            break
                        else:
                            logging.error('img/reset_account.png not found')
                            sleep(1)
                logging.error('img/ok_btn.png not found')
                sleep(1)
        else:
            return False

    def Sign_up(self, name : str, family : str):
        logging.info("Look for sign up button...")
        # Try 3 time to improve accuracy
        try_count = 0
        while try_count < 3:
            sign_up_btn = pyautogui.locateOnScreen("img/sign_up.png", confidence=0.9) # Location of sign up button on screen
            if sign_up_btn is not None:
                sign_up_btn=pyautogui.center(sign_up_btn)
                btn_x, btn_y = sign_up_btn
                logging.info('Click on last name textbox')
                pyautogui.click(btn_x,btn_y-100)
                pyautogui.write(family)
                pyautogui.press('tab')
                pyautogui.write(name)
                sleep(1)
                pyautogui.click(btn_x,btn_y)
                logging.info("Click on SIGN UP button....")
                sleep(1)
                break
            sleep(.5) # Sleep for next try

    # When register be complate and user loged in
    def Main_page(self):
        logging.info('Looking for Telegram main page')
        while pyautogui.locateOnScreen("img/tg_main.png", confidence=0.9) is None:
            sleep(.5)
        logging.info('User is now loggin')

    # After get activition code from voice mail enter it on telegram
    def Active(self, code : str):
        logging.info("Find NEXT button location")
        try_count = 0
        while try_count<3: # try to find NEXT Button
            next_btn = pyautogui.locateOnScreen("img/next_btn.png", confidence=0.9) # Location of start messaging on screen
            if next_btn is not None:
                next_btn=pyautogui.center(next_btn)

                btn_x,btn_y=next_btn
                logging.info("Enter Activation Code")
                pyautogui.click(btn_x,btn_y-160) # 160 get it in test mode. maybe need  to change it
                pyautogui.write(code)
                pyautogui.press('enter')
                logging.info("Logging to telegram...")

                self.__check_valid_code() # Check that the code entered is correct
                break
            try_count+=1
            sleep(.5)

        if try_count==3:
            logging.warning("NEXT button not found")
            exit()

    def Start(self):
        logging.info("Detect Telegram is loading...")
        if utility.RepeatFunc(20, self.__see, 1) and utility.RepeatFunc(3, self.__start, .5):
            utility.RepeatFunc(3, self.__qr_screen, .5)
        else:
            logging.error("Error in loading Telegram desktop")
            return False

        if utility.RepeatFunc(3, self.__submit_phone_number, .5):
            sleep(5)
            if utility.RepeatFunc(3, self.__banned, .2) or utility.RepeatFunc(3, self.__flood, .2):
                logging.info('{0} is banned'.format(self.phone_number))
                return False
            utility.RepeatFunc(3,self.__send_via_sms,.5)

            logging.info("Send activation code via telegram. wait 4.30 minutes")
            sleep(4*60+40) # wait for activation code
            return True
        else:
            logging.error("Start messaging button not found")
            return False


