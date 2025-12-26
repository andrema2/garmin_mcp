"""
Activity Management functions for Garmin Connect MCP Server
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
    """Register all activity management tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_activities_by_date(
        start_date: str, 
        end_date: str, 
        activity_type: str = ""
    ) -> str:
        """Get activities data between specified dates, optionally filtered by activity type
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            activity_type: Optional activity type filter (e.g., cycling, running, swimming)
            
        Returns:
            JSON string with activities or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        
        if activity_type:
            activity_type = sanitize_string(activity_type, "activity_type")
        
        activities = await call_garmin("get_activities_by_date", start_date, end_date, activity_type)
        
        if not activities:
            msg = f"No activities found between {start_date} and {end_date}"
            if activity_type:
                msg += f" for activity type '{activity_type}'"
            return msg
        
        return serialize_response(activities)

    @app.tool()
    @handle_garmin_errors
    async def get_activities_fordate(date: Optional[str] = None) -> str:
        """Get activities for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format (default: today)
            
        Returns:
            JSON string with activities or error message
        """
        date = resolve_date(date, "date")
        activities = await call_garmin("get_activities_fordate", date)
        
        if not activities:
            return f"No activities found for {date}"
        
        return serialize_response(activities)

    @app.tool()
    @handle_garmin_errors
    async def get_activity(activity_id: int) -> str:
        """Get basic activity information
        
        Args:
            activity_id: ID of the activity to retrieve (must be positive integer)
            
        Returns:
            JSON string with activity information or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        activity = await call_garmin("get_activity", activity_id)
        
        if not activity:
            return f"No activity found with ID {activity_id}"
        
        return serialize_response(activity)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_splits(activity_id: int) -> str:
        """Get splits for an activity
        
        Args:
            activity_id: ID of the activity to retrieve splits for (must be positive integer)
            
        Returns:
            JSON string with splits data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        splits = await call_garmin("get_activity_splits", activity_id)
        
        if not splits:
            return f"No splits found for activity with ID {activity_id}"
        
        return serialize_response(splits)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_typed_splits(activity_id: int) -> str:
        """Get typed splits for an activity
        
        Args:
            activity_id: ID of the activity to retrieve typed splits for (must be positive integer)
            
        Returns:
            JSON string with typed splits data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        typed_splits = await call_garmin("get_activity_typed_splits", activity_id)
        
        if not typed_splits:
            return f"No typed splits found for activity with ID {activity_id}"
        
        return serialize_response(typed_splits)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_split_summaries(activity_id: int) -> str:
        """Get split summaries for an activity
        
        Args:
            activity_id: ID of the activity to retrieve split summaries for (must be positive integer)
            
        Returns:
            JSON string with split summaries or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        split_summaries = await call_garmin("get_activity_split_summaries", activity_id)
        
        if not split_summaries:
            return f"No split summaries found for activity with ID {activity_id}"
        
        return serialize_response(split_summaries)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_weather(activity_id: int) -> str:
        """Get weather data for an activity
        
        Args:
            activity_id: ID of the activity to retrieve weather data for (must be positive integer)
            
        Returns:
            JSON string with weather data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        weather = await call_garmin("get_activity_weather", activity_id)
        
        if not weather:
            return f"No weather data found for activity with ID {activity_id}"
        
        return serialize_response(weather)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_hr_in_timezones(activity_id: int) -> str:
        """Get heart rate data in different time zones for an activity
        
        Args:
            activity_id: ID of the activity to retrieve heart rate time zone data for (must be positive integer)
            
        Returns:
            JSON string with heart rate time zone data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        hr_zones = await call_garmin("get_activity_hr_in_timezones", activity_id)
        
        if not hr_zones:
            return f"No heart rate time zone data found for activity with ID {activity_id}"
        
        return serialize_response(hr_zones)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_gear(activity_id: int) -> str:
        """Get gear data used for an activity
        
        Args:
            activity_id: ID of the activity to retrieve gear data for (must be positive integer)
            
        Returns:
            JSON string with gear data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        gear = await call_garmin("get_activity_gear", activity_id)
        
        if not gear:
            return f"No gear data found for activity with ID {activity_id}"
        
        return serialize_response(gear)

    @app.tool()
    @handle_garmin_errors
    async def get_activity_exercise_sets(activity_id: int) -> str:
        """Get exercise sets for strength training activities
        
        Args:
            activity_id: ID of the activity to retrieve exercise sets for (must be positive integer)
            
        Returns:
            JSON string with exercise sets data or error message
        """
        activity_id = validate_id(activity_id, "activity_id")
        exercise_sets = await call_garmin("get_activity_exercise_sets", activity_id)
        
        if not exercise_sets:
            return f"No exercise sets found for activity with ID {activity_id}"
        
        return serialize_response(exercise_sets)

    return app
