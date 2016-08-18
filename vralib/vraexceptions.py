
class InvalidToken(Exception):
    """Raise an invalid token """
    def __init__(self, message, payload):
        super(InvalidToken, self).__init__(message, payload)

        self.message = message
        self.payload = payload