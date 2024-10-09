class RobbieKnownException(Exception):
    """
    Parent exception class for Robbie package
    """
    user_friendly_message: str
    reason: str
    additional_help: str
    def __init__(self, user_friendly_message: str, reason: str, additional_help: str = ""):
        self.user_friendly_message = user_friendly_message
        self.reason = reason
        self.additional_help = additional_help
        

class RobbieException(Exception):
    """
    Parent exception class for Robbie package
    """
    pass

class SerializationException(RobbieException):
    """
    Exception raised when serialization errors occur.
    """
    pass

class DeserializationException(RobbieException):
    """
    Exception raised when deserialization errors occur.
    """
    pass

class DecoratorException(RobbieException):
    """
    Raised when decorator related errors are happening
    """
    pass

class RemoteCallException(RobbieException):
    """
    Raised when backend call errors are happening
    """
    pass

class RemoteFunctionException(Exception):
    """
    This is a wrapper exception to allow bubbling up of exceptions happening in a remote function call
    """
    rf_exception: Exception
    def __init__(self, e: Exception):
        self.rf_exception = e