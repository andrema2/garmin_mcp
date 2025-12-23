"""
Custom exceptions for Garmin MCP Server
"""


class GarminMCPError(Exception):
    """Base exception for all Garmin MCP errors"""
    pass


class GarminValidationError(GarminMCPError):
    """Raised when input validation fails"""
    pass


class GarminAuthenticationError(GarminMCPError):
    """Raised when authentication fails"""
    pass


class GarminAPIError(GarminMCPError):
    """Raised when Garmin API calls fail"""
    pass

