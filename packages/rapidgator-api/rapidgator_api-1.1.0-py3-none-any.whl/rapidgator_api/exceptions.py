class RapidgatorAPIError(Exception):
    """Base exception for Rapidgator API errors."""
    pass

class RapidgatorAuthenticationError(RapidgatorAPIError):
    """Raised when authentication fails."""
    pass

class RapidgatorNotFoundError(RapidgatorAPIError):
    """Raised when a requested resource is not found."""
    pass

class RapidgatorValidationError(RapidgatorAPIError):
    """Raised on validation errors."""
    pass
