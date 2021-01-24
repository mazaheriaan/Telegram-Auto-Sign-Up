import unittest
import utility
from voice import Voice
from fake_person import *
from textnow import TextNow
import warnings
import requests
from api import API
from enums import *

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

    def test_extractNumbere(self):
        self.assertEqual(utility.ExtractNumber('two zero eight once again your code is five three two zero eight goodbye'),['2','0','8','5','3','2','0','8'])
        self.assertEqual(utility.ExtractNumber('two zero eight once again your code is nine three to zero for goodbye'),['2','0','8','9','3','2','0','4'])
        self.assertEqual(utility.ExtractNumber('two zero eight once again your code is nine tree to zero for goodbye'),['2','0','8','9','3','2','0','4'])

    def test_getCode(self):
        self.assertEqual(utility.GetCodes('two zero eight once again your code is nine tree to zero for goodbye'),['93204', '93208'])
        self.assertEqual(utility.GetCodes('three five eight once again your code is nine tree to zero for goodbye'),['93204', '93304', '93254', '93208'])
        self.assertEqual(utility.GetCodes('two zero eight once again your code is five three zero zero eight goodbye'), ['53008','53208'])

# https://stackoverflow.com/a/16138561/9850815
@unittest.skip("This is ok")
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

@unittest.skip("This is ok")
class TestFakePerson(unittest.TestCase):
    def test_generate(self):
        fakePerson = FakePerson()
        result = fakePerson.Generate('Accounts/test')
        self.assertTrue(result)
        fakePerson.Close()
@unittest.skip("This is ok")
class TestTextNow(unittest.TestCase):

    def test_login(self):
        textNow = TextNow()
        if textNow.Login("sampleaccount16@gmail.com", "123456789"):
            self.assertEqual(textNow.ExtractPhoneNumber(),'4097772933')
            self.assertTrue(textNow.FindTelegramVoiceCall())
            
        #textNow.Close()

class TestAPI(unittest.TestCase):

    def test_register(self):
        api_key = '#$%lkbjflmef158@1!khbdf#$%^&asv@#$%^&ikjbasdk548785asd4f8s4f5sa1f8^ED^SE^&D&^DR*&SDR&F*S^%D*'
        url = 'https://api.membersgram.com/api/v2/fotor/register'
        data = {'phonenumber' : '989111111120','name' : 'Gholi', 'status' : 1, 'family' : 'Golavi', 'gender' : '1', 'country' : 'USA','apiKey' : api_key }
        req = requests.post(url, data=data)
        print(req.json())
        self.assertEqual(req.status_code, 200) 
        self.assertEqual(req.json()['code'], 201) # The user has already registered

    def test_get_channel(self):
        api_key = '#$%lkbjflmef158@1!khbdf#$%^&asv@#$%^&ikjbasdk548785asd4f8s4f5sa1f8^ED^SE^&D&^DR*&SDR&F*S^%D*'
        url = 'https://api.membersgram.com/api/v2/fotor/getChannel/989111111113'
        data = {'apiKey' : api_key}
        req = requests.post(url, data=data)
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.json()['code'], 200) # Succesfull geted channel
        self.assertIsNotNone(req.json()['data'])
        self.assertIsNotNone(req.json()['data']['_id'])
        self.assertIsNotNone(req.json()['data']['username'])

class  TestAPIClass(unittest.TestCase):

    def test_call_register_API(self):
        _api = API('989111111130')
        res = _api.CallRegisterAPI('Morteza', 'Saki', Gender.Man.value, 'Iran', status = TelegramRegisterStats.Succesfull.value)
        self.assertTrue(res)

if __name__ == '__main__':
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=ImportWarning)
            unittest.main()