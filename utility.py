import os
import pyautogui
import validators
import requests
import logging
from difflib import get_close_matches 

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

def closeMatches(patterns : str, word : str):
    """ Function to find all close matches of input string in given list of possible strings 

    Args:
        patterns (str): pattern that must be match
        word (str): word to be currect
    """
    return get_close_matches(word, patterns)

def Word2Number(word : str):
    """ Convert word number to number

    Args:
        word (str): your word

    >>>print(Word2Number('five'))
    5
    """
    pattern = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight","nine"]
    word = closeMatches(pattern, word)
    print(word)
    word = word[0] if len(word)>0 else None
    if word in pattern:
        return pattern.index(word)
    return None

