class FaildAPIConnection(Exception):
    """Exception raised for errors in connecto to Membersgram API

    Args:
        Exception ([type]): [description]

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    def __init__(self, messgae = "Can't connect to Membersgram API"):
        self.messgae = messgae
        super().__init__(self.messgae)

    def __str__(self):
        return self.messgae