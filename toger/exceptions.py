from typing import Optional
from . import loggers

class TogerError(Exception):
    """
    Base exception for all aiogram errors.
    """


class DetailedTogerError(TogerError):
    """
    Base exception for all aiogram errors with detailed message.
    """

    url: Optional[str] = None

    def __init__(self, message: str) -> None:
        super().__init__(message)  # Ensure Exception class is initialized
        self.message = message  # Keep the custom attribute

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class TogerAPIError(DetailedTogerError):
    """
    Base exception for all Toger API errors.
    """
    
    label: str = "Toger server says"
    
    def __init__(self, message: str) -> None:
        super().__init__(message=message)
    
    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"

class TogerBadRequest(TogerAPIError):
    """
    The standard exception for TogerBadRequest errors with a description
    """

class TogerUnauthorized(TogerAPIError):
    """
    The standard exception for TogerUnauthorized errors with a description
    """

class ValidationError(DetailedTogerError):
    """
    Input data validation error.
    """

class NotFoundMember(DetailedTogerError):
    """
    Member not found error.
    """

class TogerConflictError(TogerAPIError):
    """
    The standard exception for TogerConflictError errors with a description
    """

class TogerNetworkError(DetailedTogerError):
    """
    Network communication error.
    """

class TogerRetryAfter(DetailedTogerError):
    """
    Error with too many requests.
    """
    def __init__(self, original_message: str, chat_id: int, retry_after: int) -> None:
        message = (
            f"Retry after {retry_after} seconds.\n"
            f"Chat id: {chat_id}\n"
            f"Original message: {original_message}"
        )
        super().__init__(message)  # Ensure Exception class is properly initialized

        # Store additional attributes if needed for handling
        self.chat_id = chat_id
        self.retry_after = retry_after

class BaseMiddlewareError(DetailedTogerError):
    """
    Base exception for all middleware errors.
    """
    
    label: str = "Middleware error"
    
    def __init__(self, message: str) -> None:
        super().__init__(message)
    
    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"

class MiddlewareLimitError(BaseMiddlewareError):
    """
    Exception for middleware limit errors.
    """
