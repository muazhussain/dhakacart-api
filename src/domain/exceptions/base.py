"""Base domain exception."""


class DomainException(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str = "A domain error occured") -> None:
        self.message = message
        super().__init__(self.message)
