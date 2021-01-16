import unittest
import utility
from voice import Voice

class TestUtility(unittest.TestCase):
    def test_word2number(self):
        self.assertEqual(utility.Word2Number("zero"),0)
        self.assertEqual(utility.Word2Number("one"),1)
        self.assertEqual(utility.Word2Number("two"),2)
        self.assertEqual(utility.Word2Number("to"),2)
        self.assertEqual(utility.Word2Number("three"),3)
        self.assertEqual(utility.Word2Number("tree"),3)
        self.assertEqual(utility.Word2Number("four"),4)
        self.assertEqual(utility.Word2Number("for"),4)
        self.assertEqual(utility.Word2Number("five"),5)
        self.assertEqual(utility.Word2Number("faive"),5)
        self.assertEqual(utility.Word2Number("six"),6)
        self.assertEqual(utility.Word2Number("sex"),6)
        self.assertEqual(utility.Word2Number("seven"),7)
        self.assertEqual(utility.Word2Number("even"),7)
        self.assertEqual(utility.Word2Number("eight"),8)
        self.assertEqual(utility.Word2Number("nine"),9)


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

if __name__ == '__main__':
    unittest.main()