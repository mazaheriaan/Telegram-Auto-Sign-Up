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

def Word2Number(word : str):
    """ Convert word number to number

    Args:
        word (str): your word

    >>>print(Word2Number('five one one once again your code is one one five one one goodbye'))
    5 1 1 once again your code is 1 1 5 1 1 goodbye
    """
    units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight","nine"]
    for (i, w) in enumerate(units, start = 0):
        word = word.replace(w, str(i))
    
    return word
