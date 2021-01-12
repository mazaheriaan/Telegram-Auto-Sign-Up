import os

def CreateDirectory(path : str):
    try:
        os.mkdir(path)
        return True
    except:
        return False