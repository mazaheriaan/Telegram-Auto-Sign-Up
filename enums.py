import enum

class RegisterAPIStatus(enum.Enum):
    Succesfull : 200
    AlreadyJoined : 201

class Gender(enum.enum):
    Man : 0
    Woman : 1