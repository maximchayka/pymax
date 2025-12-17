"""Error types for Max Bot API client."""

from typing import Any


class MaxBotError(Exception):
    """Base exception for Max Bot API client."""

    pass


class EmptyTokenError(MaxBotError):
    """Raised when bot token is empty."""

    def __init__(self) -> None:
        super().__init__("bot token is empty")


class InvalidURLError(MaxBotError):
    """Raised when API URL is invalid."""

    def __init__(self, url: str = "") -> None:
        super().__init__(f"invalid API URL: {url}" if url else "invalid API URL")


class APIError(MaxBotError):
    """Error returned by the API."""

    def __init__(self, code: str, message: str, details: Any = None) -> None:
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"API error [{code}]: {message}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, APIError):
            return self.code == other.code
        return False


class NetworkError(MaxBotError):
    """Error during network operation."""

    def __init__(self, operation: str, cause: Exception) -> None:
        self.operation = operation
        self.cause = cause
        super().__init__(f"network error during {operation}: {cause}")


class TimeoutError(MaxBotError):
    """Timeout error during operation."""

    def __init__(self, operation: str, reason: str = "") -> None:
        self.operation = operation
        self.reason = reason
        message = f"timeout during {operation}"
        if reason:
            message += f": {reason}"
        super().__init__(message)

    def timeout(self) -> bool:
        return True


class SerializationError(MaxBotError):
    """Error during data serialization/deserialization."""

    def __init__(self, operation: str, data_type: str, cause: Exception) -> None:
        self.operation = operation
        self.data_type = data_type
        self.cause = cause
        super().__init__(f"serialization error during {operation} of {data_type}: {cause}")
