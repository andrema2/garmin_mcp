"""
Weight management functions for Garmin Connect MCP Server
"""
import logging
from datetime import datetime, timezone
from typing import Optional

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import (
    validate_date,
    validate_date_range,
    validate_positive_number,
    resolve_date,
    sanitize_string,
)

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all weight management tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_weigh_ins(start_date: str, end_date: str) -> str:
        """Get weight measurements between specified dates
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with weight measurements or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        weigh_ins = await call_garmin("get_weigh_ins", start_date, end_date)
        
        if not weigh_ins:
            return f"No weight measurements found between {start_date} and {end_date}."
        
        return serialize_response(weigh_ins)

    @app.tool()
    @handle_garmin_errors
    async def get_daily_weigh_ins(date: Optional[str] = None) -> str:
        """Get weight measurements for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with weight measurements or error message
        """
        date = resolve_date(date, "date")
        weigh_ins = await call_garmin("get_daily_weigh_ins", date)
        
        if not weigh_ins:
            return f"No weight measurements found for {date}."
        
        return serialize_response(weigh_ins)
    
    @app.tool()
    @handle_garmin_errors
    async def delete_weigh_ins(date: str, delete_all: bool = True) -> str:
        """Delete weight measurements for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            delete_all: Whether to delete all measurements for the day
            
        Returns:
            Deletion result or error message
        """
        date = validate_date(date, "date")
        result = await call_garmin("delete_weigh_ins", date, delete_all=delete_all)
        return serialize_response(result) if not isinstance(result, str) else result
    
    @app.tool()
    @handle_garmin_errors
    async def add_weigh_in(weight: float, unit_key: str = "kg") -> str:
        """Add a new weight measurement
        
        Args:
            weight: Weight value (must be positive)
            unit_key: Unit of weight ('kg' or 'lb')
            
        Returns:
            Addition result or error message
        """
        weight = validate_positive_number(weight, "weight", allow_zero=False)
        unit_key = sanitize_string(unit_key, "unit_key")
        
        if unit_key not in ("kg", "lb"):
            raise ValueError(f"unit_key must be 'kg' or 'lb', got '{unit_key}'")
        
        result = await call_garmin("add_weigh_in", weight=weight, unitKey=unit_key)
        return serialize_response(result) if not isinstance(result, str) else result
    
    @app.tool()
    @handle_garmin_errors
    async def add_weigh_in_with_timestamps(
        weight: float, 
        unit_key: str = "kg", 
        date_timestamp: str = None, 
        gmt_timestamp: str = None
    ) -> str:
        """Add a new weight measurement with specific timestamps
        
        Args:
            weight: Weight value (must be positive)
            unit_key: Unit of weight ('kg' or 'lb')
            date_timestamp: Local timestamp in format YYYY-MM-DDThh:mm:ss (optional)
            gmt_timestamp: GMT timestamp in format YYYY-MM-DDThh:mm:ss (optional)
            
        Returns:
            Addition result or error message
        """
        weight = validate_positive_number(weight, "weight", allow_zero=False)
        unit_key = sanitize_string(unit_key, "unit_key")
        
        if unit_key not in ("kg", "lb"):
            raise ValueError(f"unit_key must be 'kg' or 'lb', got '{unit_key}'")
        
        if date_timestamp is None or gmt_timestamp is None:
            # Generate timestamps if not provided (FIXED: use timezone-aware datetime)
            now = datetime.now(timezone.utc)
            date_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S')
            gmt_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S')
        
        result = await call_garmin(
            "add_weigh_in_with_timestamps",
            weight=weight,
            unitKey=unit_key,
            dateTimestamp=date_timestamp,
            gmtTimestamp=gmt_timestamp
        )
        return serialize_response(result) if not isinstance(result, str) else result

    return app
