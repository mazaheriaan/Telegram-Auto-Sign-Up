# By Morteza Jan 3 2021
import validators
import re
from time import sleep
import ps
import os
import shutil
import sys
import doctest
import logging
import utility
from voice import Voice
from textnow import TextNow
from telegram_desktop import TelegramDesktop
from fake_person import FakePerson


# Set logging in info mode
logging.getLogger().setLevel(logging.INFO)


# Global variable
tg_desktop = '' # telegram desktop process.
phone_number = '+1'
tg_cli = '' # Telegram-cli process
ps_log = '' # keep_log.sh process

def CheckInput(email : str, password : str) :
    """Check and validate input.

    >>> print(CheckInput("test@gmail.com","1234567")) # Everythin is OK
    True
    >>> print(CheckInput("testgmail.com","1234567")) # Wrong Email
    False
    >>> print(CheckInput("test@gmail.com","")) # Empty Password
    False
    """

    if validators.email(email) and password:
        return True
    else:
        return False


def TelegramCLI():
    global phone_number
    global tg_cli

    profile_path = '{0}/Accounts/{1}/telegram_cli'.format(os.getcwd,phone_number)

    def Profile():
        def Config():
            def Create():            
                new_user_config = '''
{0} = {{
config_directory = "{1}";
msg_num = true;
}};'''
                new_user_config.format(phone_number,profile_path)

                with open(r'~/.telegram-cli/config','a') as tg_cli_config:
                    tg_cli_config.write(new_user_config)

                logging.info('Telegram-cli config create at ~/.telegram-cli/config for new %s user' %(phone_number))

            def Remove():
                if os.path.isdir(profile_path):
                    shutil.rmtree(profile_path)
                    logging.info('Old telegram-cli config for %s was removed' %(phone_number))

        def Start():            
            tg_cli = ps.start("telegram-cli -p {0} -k tg-server.pub -W".format(phone_number))
            logging.info('Telegram-cli for {0} user was started'.format(phone_number))

        def Logging(): # Track Telegram logs include notification for extract activitation code
            global ps_log

            def Start():
                ps_log = ps.start("bash keep_log.sh")
                logging.info('Start logging Telegram desktop notification for find activation code')

def Main():
    doctest.testmod()
    if len(sys.argv) >= 3:
        textnow_username = sys.argv[1]
        textnow_password = sys.argv[2]

        logging.info('Start {0} account...'.format(textnow_username))
        logging.info("Switch to secondary desktop...")
        #utility.SwitchDesktop(1)

        txtNow = TextNow()
        if txtNow.Login(textnow_username, textnow_password):
            txtNow.AreaCode()
            txtNow.TermAccept()
            phone_number = utility.RepeatFunc( 3, txtNow.ExtractPhoneNumber)
            if phone_number is not None:
                tg_desktop = TelegramDesktop(phone_number)
                if tg_desktop.Start():
                # Wait 4.30 minutes until get activitation code

                    if utility.RepeatFunc(10,txtNow.FindTelegramVoiceCall):
                        sleep(5)
                        voice_address = utility.RepeatFunc(3, txtNow.DownloadVoiceMail)
                        if voice_address is not None:                
                            new_voice = Voice(voice_address)
                            logging.info('Boost voice mail...')
                            new_voice.Boost()
                            logging.info('Save boosted voice')
                            new_voice.Save(voice_address)
                            text_from_voice = new_voice.Recognize(voice_address)
                            logging.info('Voise is : %s' %(text_from_voice))
                            codes = utility.GetCodes(text_from_voice)
                            logging.info('Codes is %s' %(codes))
                            tg_desktop.Active(codes[0])
                            utility.RepeatFunc(3,tg_desktop.Forget_password)

                            fakePerson = FakePerson()
                            fakePerson = fakePerson.Generate('Accounts/%s' %(phone_number))
                            tg_desktop.Sign_up(fakePerson[1],fakePerson[2])

                            tg_desktop.Main_page()
                    else:
                        logging.info('Account has password')
                        ps.terminate(tg_desktop)


        #tg_activation_code = TextNow(textnow_username,textnow_password)

        
        # disable until find a method to get 100 percent accuracy
        # SubmitCodeTG(tg_activation_code)
        # ForgetPassword()
        # GenerateFakePerson()
        # browser.close()
        # sleep(3)
        # TgMainPage()
        # logging.info('Complate sign up')
        #ps.terminate(tg_desktop)
    else:
        logging.error("Error in inputs")
        print("Please enter all inputs.\nemail password phone_number")
        exit()

if __name__ == "__main__":
    Main()


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