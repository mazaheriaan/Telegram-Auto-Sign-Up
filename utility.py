import os
import pyautogui
import validators
import requests
import logging

def CreateDirectory(path : str):
    try:
        os.mkdir(path)
        return True
    except:
        return False

def SwitchDesktop(desktop_number : int):
    if desktop_number == 1:
        pyautogui.hotkey('winleft','pagedown')
    else:
        pyautogui.hotkey('winleft','pageup')

def DownloadFile(address : str, account : str, fileName : str):
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