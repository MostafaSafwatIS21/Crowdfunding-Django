class CrowdfundingException(Exception):
    """Base exception class for all custom crowdfunding application errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationException(CrowdfundingException):
    """Exception raised when input validation fails."""
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message)
        self.errors = errors or {}
