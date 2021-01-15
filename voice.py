from pydub import AudioSegment
import speech_recognition as sr
import os

class Voice:
    def __init__(self, sound_address : str):
        if os.path.exists(sound_address) and sound_address.endswith('.wav'):
            with open(sound_address, 'rb') as f:
                self.sound = AudioSegment.from_wav(f)
        else:
            raise "Invalid file"

    def Cut(self, start : float = 0, end : float = -1):
        self.sound = self.sound[start:end]
        return len(self.sound)

    def Boost(self, value : int = 8):
        self.sound = self.sound + value

    def Save(self, output : str, format : str = 'wav' ):
        out = self.sound.export(output,format=format)
        out.close()
        return output

    def Recognize(self, sound_address : str):
        api_key = 'HVET3LMFZFTAX55M3NQMHORLEMIWFE25'

        r = sr.Recognizer()
        with sr.AudioFile(sound_address) as source:
            audio_text = r.listen(source)
                
            # using wit speech recognition
            r.adjust_for_ambient_noise(source, duration=1)
            text = r.recognize_wit(audio_text, key= api_key)
            return text