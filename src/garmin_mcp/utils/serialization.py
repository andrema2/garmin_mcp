"""
Serialization utilities for MCP responses
"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def serialize_response(data: Any) -> str:
    """Serialize Python objects to JSON string for MCP responses
    
    Args:
        data: Python object to serialize (dict, list, str, None, etc.)
        
    Returns:
        JSON string representation of the data
        
    Examples:
        >>> serialize_response({"key": "value"})
        '{\\n  "key": "value"\\n}'
        
        >>> serialize_response([1, 2, 3])
        '[\\n  1,\\n  2,\\n  3\\n]'
        
        >>> serialize_response("simple string")
        'simple string'
        
        >>> serialize_response(None)
        'null'
    """
    if data is None:
        return "null"
    
    # If already a string, return as-is (assuming it's already formatted)
    if isinstance(data, str):
        return data
    
    try:
        # Serialize to JSON with pretty formatting
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        logger.error(f"Serialization error: {e}", exc_info=True)
        return f"Error serializing response: {str(e)}"

