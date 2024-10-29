"""
Custom exceptions to celery_tasks app.
"""


class RetryLaterException(Exception):
    """Exception raised when API return retry later error."""
    def __init__(self, message):
        super().__init__(message)
