from pydub import AudioSegment
import speech_recognition as sr
import os

class Voice:
    def __init__(self, sound_address : str):
        if os.path.exists(sound_address) and sound_address.endswith('.wav'):
            self.sound = AudioSegment.from_wav(sound_address)
        else:
            raise "Invalid file"

    def Cut(start : float = 0, end : float = -1):
        self.sound = self.sound[start:end]

    def Save(output : str, format : str = 'wav' ):
        self.sound.export(output,format=format)

