import requests
from errors import *
from enums import *

class API:

    def __init__(self, phone_number : str):
        self.phone_number = phone_number
        self.api_key = '#$%lkbjflmef158@1!khbdf#$%^&asv@#$%^&ikjbasdk548785asd4f8s4f5sa1f8^ED^SE^&D&^DR*&SDR&F*S^%D*'

    def CallRegisterAPI(self, name : str, family : str, gender : int, country : str, *, status : int):
        gender = '0' if gender == 'man' else '1'
        url = 'https://api.membersgram.com/api/v2/fotor/register'
        data = {'phonenumber' : self.phone_number,'name' : name, 'status' : status, 'family' : family, 'gender' : gender, 'country' : country, 'apiKey' : self.api_key }
        req = requests.post(url, data=data)

        if req.status_code == 200:
            res_status = req.json()['code']
            if res_status == RegisterAPIStatus.Succesfull.value:
                self.SaveAccountInfo(self.phone_number, name, family, gender, country, str(status), str(res_status))
                return True
            return False
        raise FaildAPIConnection() # Error when can't connect to Membersgram api

    def SaveAccountInfo(self, *argv):
        with open('Accounts/%s/info.txt' %(self.phone_number),'w') as f:
            f.write('\n'.join(argv))