import os
import pyautogui
import validators
import requests
import logging
from difflib import get_close_matches 
from time import sleep
import re

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

def DownloadFile(address : str,dest : str):
    if validators.url(address):        
        req = requests.get(address)

        if req.status_code == 200:
            dest_file = '{0}/{1}'.format(os.getcwd(), dest)
            logging.info("Save file on {0}/{1}".format(os.getcwd(), dest))
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
    ignore_words = ['once', 'your']
    if word not in ignore_words:
        word = closeMatches(pattern, word)
    word = word[0] if len(word)>0 else None
    if word in pattern:
        return pattern.index(word)
    return None

def ExtractNumber(text : str):
    words = text.split()
    result = []
    for word in words:
        num = Word2Number(word)
        if num is not None:
            result.append(str(num))
    return result

def GetCodes(text : str):
    numbers = ExtractNumber(text)
    code1 = ''.join(numbers[-5:])

    code2 = numbers[-5:-1 * (len(numbers)-5)] + numbers[:-5]
    
    result = []
    result.append(code1)
    for i in range(len(code1)):
        if code1[i] != code2[i]:
            new_code = numbers[-5:]
            new_code[i] = code2[i]
            result.append(''.join(new_code))
    
    print(result)
    return result

# https://stackoverflow.com/a/9048049/9850815
def RepeatFunc(times, f, wait = .5):
    for i in range(times):
        res = f()
        if res:
            return res
        sleep(wait)
    return False

def RemoveParenthesisFromPhone(phone_number : str):
    phone_number = ''.join(re.findall('\d+',phone_number))
    return phone_number

    