"""
Women's health functions for Garmin Connect MCP Server
"""
import logging
from typing import Optional

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import validate_date, validate_date_range, resolve_date

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all women's health tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_pregnancy_summary() -> str:
        """Get pregnancy summary data
        
        Returns:
            JSON string with pregnancy summary or error message
        """
        summary = await call_garmin("get_pregnancy_summary")
        if not summary:
            return "No pregnancy summary data found."
        return serialize_response(summary)
    
    @app.tool()
    @handle_garmin_errors
    async def get_menstrual_data_for_date(date: Optional[str] = None) -> str:
        """Get menstrual data for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with menstrual data or error message
        """
        date = resolve_date(date, "date")
        data = await call_garmin("get_menstrual_data_for_date", date)
        
        if not data:
            return f"No menstrual data found for {date}."
        return serialize_response(data)
    
    @app.tool()
    @handle_garmin_errors
    async def get_menstrual_calendar_data(start_date: str, end_date: str) -> str:
        """Get menstrual calendar data between specified dates
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with menstrual calendar data or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        data = await call_garmin("get_menstrual_calendar_data", start_date, end_date)
        
        if not data:
            return f"No menstrual calendar data found between {start_date} and {end_date}."
        return serialize_response(data)

    return app
