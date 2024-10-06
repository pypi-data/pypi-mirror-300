class AppartmeError(Exception):
    """Base exception for Appartme errors."""


class DeviceOfflineError(AppartmeError):
    """Exception raised when a device is offline."""


class ApiError(AppartmeError):
    """Exception raised for general API errors."""
