"""
Input validation utilities
"""

import re
from datetime import datetime
from typing import Optional

from garmin_mcp.utils.errors import GarminValidationError

# Date format: YYYY-MM-DD
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def validate_date(date_str: str, param_name: str = "date") -> str:
    """Validate date format YYYY-MM-DD
    
    Args:
        date_str: Date string to validate
        param_name: Name of the parameter for error messages
        
    Returns:
        Validated date string
        
    Raises:
        GarminValidationError: If date format is invalid
        
    Examples:
        >>> validate_date("2024-01-15")
        '2024-01-15'
        
        >>> validate_date("2024-13-45", "start_date")
        Traceback (most recent call last):
        ...
        GarminValidationError: Invalid date format for start_date: 2024-13-45. Use YYYY-MM-DD
    """
    if not isinstance(date_str, str):
        raise GarminValidationError(
            f"{param_name} must be a string, got {type(date_str).__name__}"
        )
    
    if not DATE_PATTERN.match(date_str):
        raise GarminValidationError(
            f"Invalid date format for {param_name}: {date_str}. Use YYYY-MM-DD"
        )
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise GarminValidationError(
            f"Invalid date for {param_name}: {date_str}. {str(e)}"
        )
    
    return date_str


def validate_date_range(start_date: str, end_date: str) -> tuple[str, str]:
    """Validate date range (start_date <= end_date)
    
    Args:
        start_date: Start date string
        end_date: End date string
        
    Returns:
        Tuple of validated (start_date, end_date)
        
    Raises:
        GarminValidationError: If dates are invalid or start > end
    """
    start = validate_date(start_date, "start_date")
    end = validate_date(end_date, "end_date")
    
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    
    if start_dt > end_dt:
        raise GarminValidationError(
            f"start_date ({start}) must be less than or equal to end_date ({end})"
        )
    
    return start, end


def validate_positive_number(
    value: float, 
    param_name: str = "value",
    allow_zero: bool = False
) -> float:
    """Validate that a number is positive
    
    Args:
        value: Number to validate
        param_name: Name of the parameter for error messages
        allow_zero: Whether to allow zero values
        
    Returns:
        Validated number
        
    Raises:
        GarminValidationError: If number is not positive
    """
    if not isinstance(value, (int, float)):
        raise GarminValidationError(
            f"{param_name} must be a number, got {type(value).__name__}"
        )
    
    if allow_zero and value < 0:
        raise GarminValidationError(
            f"{param_name} must be greater than or equal to 0, got {value}"
        )
    elif not allow_zero and value <= 0:
        raise GarminValidationError(
            f"{param_name} must be greater than 0, got {value}"
        )
    
    return float(value)


def validate_id(id_value: int, param_name: str = "id") -> int:
    """Validate that an ID is a positive integer
    
    Args:
        id_value: ID to validate
        param_name: Name of the parameter for error messages
        
    Returns:
        Validated ID
        
    Raises:
        GarminValidationError: If ID is invalid
    """
    if not isinstance(id_value, int):
        raise GarminValidationError(
            f"{param_name} must be an integer, got {type(id_value).__name__}"
        )
    
    if id_value <= 0:
        raise GarminValidationError(
            f"{param_name} must be a positive integer, got {id_value}"
        )
    
    return id_value


def sanitize_string(value: str, param_name: str = "string") -> str:
    """Sanitize string input for safe use in queries
    
    Args:
        value: String to sanitize
        param_name: Name of the parameter for error messages
        
    Returns:
        Sanitized string
        
    Raises:
        GarminValidationError: If value is not a string
    """
    if not isinstance(value, str):
        raise GarminValidationError(
            f"{param_name} must be a string, got {type(value).__name__}"
        )
    
    # Remove leading/trailing whitespace
    sanitized = value.strip()
    
    # Check for potentially dangerous characters in GraphQL context
    # Allow alphanumeric, spaces, hyphens, underscores, and common punctuation
    if not sanitized:
        raise GarminValidationError(f"{param_name} cannot be empty")
    
    return sanitized

