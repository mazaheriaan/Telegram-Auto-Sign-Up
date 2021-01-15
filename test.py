import unittest
import utility
from voice import Voice

class TestUtility(unittest.TestCase):
    def test_word2number(self):
        result = utility.Word2Number("five one one once again your code is one one five one one goodbye")
        self.assertEqual(result,"5 1 1 once again your code is 1 1 5 1 1 goodbye")

class TestVoice(unittest.TestCase):
    
    def test_cut(self):
        voice = Voice('sound.wav')
        self.assertEqual(voice.Cut(),13799)
        self.assertEqual(voice.Cut(6*1000,13*1000),7000)

    def test_recognize(self):
        voice = Voice('sound.wav')
        voice.Boost()
        boost = voice.Save('sound_boost.wav')
        self.assertEqual(voice.Recognize(boost), 'two zero eight once again your code is five three two zero eight goodbye')

        voice2 = Voice('Accounts/4097772933/voice.wav')
        voice2.Boost()
        boost2 = voice2.Save('sound_boost.wav')
        self.assertEqual(voice2.Recognize(boost2), 'zero nine three eight once again your code is nine zero nine three eight goodbye')

        voice3 = Voice('Accounts/6137065830/voice.wav')
        voice3.Boost()
        boost3 = voice2.Save('sound_boost.wav')
        self.assertEqual(voice3.Recognize(boost3), 'eight six eight three goodbye eight six eight three goodbye')

if __name__ == '__main__':
    unittest.main()