from exceptions.base import CrowdfundingException

class EmailAlreadyExistsException(CrowdfundingException):
    """Exception raised when registering an email that is already registered."""
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' is already registered.")
        self.email = email


class InvalidCredentialsException(CrowdfundingException):
    """Exception raised when login credentials do not match."""
    def __init__(self):
        super().__init__("Invalid email or password.")


class UserNotFoundException(CrowdfundingException):
    """Exception raised when a user is searched but not found."""
    def __init__(self, identifier: str):
        super().__init__(f"User not found: {identifier}")
        self.identifier = identifier
