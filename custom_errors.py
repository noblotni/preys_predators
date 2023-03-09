"""Define custom errors for the project."""


class UnsupportedMovingMethodError(Exception):
    """Error raised when agents specified moving method is not supported."""

    def __init__(self):
        pass
