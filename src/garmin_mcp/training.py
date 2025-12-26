"""
Training and performance functions for Garmin Connect MCP Server
"""
import logging
from typing import Optional

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import (
    validate_date,
    validate_date_range,
    validate_id,
    resolve_date,
    sanitize_string,
)

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all training-related tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_progress_summary_between_dates(
        start_date: str, end_date: str, metric: str
    ) -> str:
        """Get progress summary for a metric between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            metric: Metric to get progress for (e.g., "elevationGain", "duration", "distance", "movingDuration")
            
        Returns:
            JSON string with progress summary or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        metric = sanitize_string(metric, "metric")
        summary = await call_garmin("get_progress_summary_between_dates", start_date, end_date, metric)
        if not summary:
            return f"No progress summary found for {metric} between {start_date} and {end_date}."
        return serialize_response(summary)
    
    @app.tool()
    @handle_garmin_errors
    async def get_hill_score(start_date: str, end_date: str) -> str:
        """Get hill score data between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with hill score data or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        hill_score = await call_garmin("get_hill_score", start_date, end_date)
        
        if not hill_score:
            return f"No hill score data found between {start_date} and {end_date}."
        return serialize_response(hill_score)
    
    @app.tool()
    @handle_garmin_errors
    async def get_endurance_score(start_date: str, end_date: str) -> str:
        """Get endurance score data between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with endurance score data or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        endurance_score = await call_garmin("get_endurance_score", start_date, end_date)
        
        if not endurance_score:
            return f"No endurance score data found between {start_date} and {end_date}."
        return serialize_response(endurance_score)
    
    @app.tool()
    @handle_garmin_errors
    async def get_training_effect(activity_id: int) -> str:
        """Get training effect data for a specific activity
        
        Args:
            activity_id: ID of the activity to retrieve training effect for (must be positive integer)
            
        Returns:
            JSON string with training effect data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        effect = await call_garmin("get_training_effect", activity_id)
        
        if not effect:
            return f"No training effect data found for activity with ID {activity_id}."
        return serialize_response(effect)
    
    @app.tool()
    @handle_garmin_errors
    async def get_max_metrics(date: Optional[str] = None) -> str:
        """Get max metrics data (like VO2 Max and fitness age)
        
        Args:
            date: Date in YYYY-MM-DD format (default: today)
            
        Returns:
            JSON string with max metrics data or error message
        """
        date = resolve_date(date, "date")
        metrics = await call_garmin("get_max_metrics", date)
        
        if not metrics:
            return f"No max metrics data found for {date}."
        return serialize_response(metrics)
    
    @app.tool()
    @handle_garmin_errors
    async def get_hrv_data(date: Optional[str] = None) -> str:
        """Get Heart Rate Variability (HRV) data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with HRV data or error message
        """
        date = resolve_date(date, "date")
        hrv_data = await call_garmin("get_hrv_data", date)
        
        if not hrv_data:
            return f"No HRV data found for {date}."
        return serialize_response(hrv_data)
    
    @app.tool()
    @handle_garmin_errors
    async def get_fitnessage_data(date: Optional[str] = None) -> str:
        """Get fitness age data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with fitness age data or error message
        """
        date = resolve_date(date, "date")
        fitness_age = await call_garmin("get_fitnessage_data", date)
        
        if not fitness_age:
            return f"No fitness age data found for {date}."
        return serialize_response(fitness_age)
    
    @app.tool()
    @handle_garmin_errors
    async def request_reload(date: Optional[str] = None) -> str:
        """Request reload of epoch data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Reload result or error message
        """
        date = resolve_date(date, "date")
        result = await call_garmin("request_reload", date)
        return serialize_response(result) if not isinstance(result, str) else result

    return app
