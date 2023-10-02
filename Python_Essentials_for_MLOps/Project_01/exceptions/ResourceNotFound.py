class ResourceNotFound(Exception):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message):
        super().__init__(message)