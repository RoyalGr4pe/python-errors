class EndpointError(Exception):
    """
    Custom exception for handling errors in endpoints.
    """
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code


class InvalidRateLimit(Exception):
    """
    
    """
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return self.message