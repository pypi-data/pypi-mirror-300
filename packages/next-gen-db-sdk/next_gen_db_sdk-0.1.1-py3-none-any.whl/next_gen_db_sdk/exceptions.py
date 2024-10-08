class NextGenDBError(Exception):
    """General exception for next-gen-db errors."""
    pass

class NotFoundError(NextGenDBError):
    """Raised when a resource is not found in the database."""
    pass

