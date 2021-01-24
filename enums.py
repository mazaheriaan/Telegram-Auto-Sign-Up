import enum

class RegisterAPIStatus(enum.Enum):
    Succesfull = 200
    AlreadyJoined = 201

class Gender(enum.Enum):
    Man = 0
    Woman = 1

class TelegramRegisterStats(enum.Enum):
    Succesfull = 1
    Ban = 2
    Flood = 3
    HasPassword = 4