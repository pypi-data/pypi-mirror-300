# exceptions.py
class BeamdustError(Exception):
    """Base class for all Beamdust errors."""
    pass

class LoginError(BeamdustError):
    """Exception raised for login-related errors."""
    def __init__(self, message="Login failed"):
        super().__init__(message)

class APICallError(BeamdustError):
    """Exception raised for errors during API calls."""
    def __init__(self, message="API call failed", status_code=None, response=None):
        self.status_code = status_code
        self.response = response
        super().__init__(f"{message} (Status Code: {status_code})" if status_code else message)

class MethodNotFoundError(BeamdustError):
    """Exception raised when a method is not found."""
    def __init__(self, method_name):
        super().__init__(f"The method {method_name} does not exist in Beamdust. Use get_available_functions() to list available functions.")
