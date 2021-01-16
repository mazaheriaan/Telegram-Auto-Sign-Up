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

    if len(numbers) == 8:
        code2 = numbers[-5:-3] + numbers[:-5]
    elif len(numbers) == 7:
        code2 = numbers[-5:-2] + numbers[:-5]
    else:
        raise Exception("Exctracted code is invalid")

    result = []
    result.append(code1)
    for i in range(len(code1)):
        if code1[i] != code2[i]:
            new_code = numbers[-5:]
            new_code[i] = code2[i]
            result.append(''.join(new_code))
    
    print(result)
    return result


    