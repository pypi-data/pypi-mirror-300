"""
This module defines custom exceptions for the SomeComfort library.

These exceptions are used to handle specific errors that may occur when interacting
with the SomeComfort API or devices, such as authentication failures, rate limiting,
invalid parameters, or API errors.
"""

class SomeComfortError(Exception):
    """
    Base exception for the SomeComfort library.

    All other exceptions inherit from this class. It is used for general errors
    that do not fit into the more specific exception categories.
    """


class AuthError(SomeComfortError):
    """
    Raised when there is an authentication failure.

    This error occurs when the provided credentials are invalid or when
    there are issues logging in to the SomeComfort service.
    """


class APIError(SomeComfortError):
    """
    Raised when an error occurs while communicating with the API.

    This can include issues like unexpected responses, invalid API endpoints, or
    errors returned by the API itself.
    """


class SessionTimedOut(SomeComfortError):
    """
    Raised when the session times out due to inactivity or other factors.

    This error indicates that the user's session has expired and must be
    re-authenticated.
    """


class TooManyAttemptsError(SomeComfortError):
    """
    Raised when too many login attempts have been made.

    This error is triggered when the user or system exceeds the number of allowed
    login attempts, possibly leading to a temporary lockout.
    """


class APIRateLimited(SomeComfortError):
    """
    Raised when the API rate limit is reached.

    This error indicates that the user or system has exceeded the allowed number
    of API requests within a certain time window.
    """

    def __init__(self):
        """
        Initializes the APIRateLimited error with a default message.
        """
        super().__init__('You are being rate-limited. Try waiting a bit.')


class DeviceNotFoundError(SomeComfortError):
    """
    Raised when a requested device cannot be found.

    This error occurs when the system is unable to locate a device that was
    requested, either because it doesn't exist or is no longer available.
    """


class InvalidParameterError(SomeComfortError):
    """
    Raised when an invalid parameter is provided to a function or API request.

    This error is triggered when a parameter does not meet the required
    specifications, such as incorrect data types or out-of-range values.
    """


class InvalidResponseError(SomeComfortError):
    """
    Raised when the API returns an unexpected or invalid response.

    This error occurs when the response from the SomeComfort API is not in the
    expected format or contains invalid data.
    """
