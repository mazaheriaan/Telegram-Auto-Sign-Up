import enum

class RegisterAPIStatus(enum.Enum):
    Succesfull : 200
    AlreadyJoined : 201

class Gender(enum.enum):
    Man : 0
    Woman : 1

class TelegramRegisterStats(enum.Enum):
    Register :  1
    Ban : 2
    Flood : 3
    HasPassword : 4