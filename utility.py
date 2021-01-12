import os
import pyautogui

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