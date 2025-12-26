"""
Workout-related functions for Garmin Connect MCP Server
"""
import logging

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import validate_date, validate_date_range, validate_id

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all workout-related tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_workouts() -> str:
        """Get all workouts
        
        Returns:
            JSON string with all workouts or error message
        """
        workouts = await call_garmin("get_workouts")
        if not workouts:
            return "No workouts found."
        return serialize_response(workouts)
    
    @app.tool()
    @handle_garmin_errors
    async def get_workout_by_id(workout_id: int) -> str:
        """Get details for a specific workout
        
        Args:
            workout_id: ID of the workout to retrieve (must be positive integer)
            
        Returns:
            JSON string with workout details or error message
        """
        workout_id = validate_id(workout_id, "workout_id")
        workout = await call_garmin("get_workout_by_id", workout_id)
        if not workout:
            return f"No workout found with ID {workout_id}."
        return serialize_response(workout)
    
    @app.tool()
    @handle_garmin_errors
    async def download_workout(workout_id: int) -> str:
        """Download a workout as a FIT file (this will return a message about how to access the file)
        
        Args:
            workout_id: ID of the workout to download (must be positive integer)
            
        Returns:
            Message about workout data availability
        """
        workout_id = validate_id(workout_id, "workout_id")
        workout_data = await call_garmin("download_workout", workout_id)
        if not workout_data:
            return f"No workout data found for workout with ID {workout_id}."
        
        # Since we can't return binary data directly, we'll inform the user
        return f"Workout data for ID {workout_id} is available. The data is in FIT format and would need to be saved to a file."
    
    @app.tool()
    @handle_garmin_errors
    async def upload_workout(workout_json: str) -> str:
        """Upload a workout from JSON data
        
        Args:
            workout_json: JSON string containing workout data
            
        Returns:
            Upload result or error message
        """
        from garmin_mcp.utils.validation import sanitize_string
        
        workout_json = sanitize_string(workout_json, "workout_json")
        result = await call_garmin("upload_workout", workout_json)
        return serialize_response(result) if not isinstance(result, str) else result
            
    @app.tool()
    @handle_garmin_errors
    async def upload_activity(file_path: str) -> str:
        """Upload an activity from a file
        
        Note: This functionality is not currently supported in MCP server mode
        due to file access limitations.

        Args:
            file_path: Path to the activity file (.fit, .gpx, .tcx)
            
        Returns:
            Error message indicating unsupported functionality
        """
        # This is intentionally not implemented - file operations require special handling
        # that is not compatible with MCP server stdio communication
        return "Activity upload from file is not supported in this MCP server implementation. Please use the Garmin Connect web interface or mobile app."

    @app.tool()
    @handle_garmin_errors
    async def get_scheduled_workouts(start_date: str, end_date: str) -> str:
        """Get scheduled workouts between two dates.

        Returns workouts that have been scheduled on the Garmin Connect calendar,
        including their scheduled dates.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with scheduled workouts or error message
        """
        # Validate dates (this also prevents GraphQL injection)
        start_date, end_date = validate_date_range(start_date, end_date)
        
        # Use GraphQL variables to prevent injection (SECURITY FIX)
        query = {
            "query": """
                query($startDate: String!, $endDate: String!) {
                    workoutScheduleSummariesScalar(startDate: $startDate, endDate: $endDate)
                }
            """,
            "variables": {
                "startDate": start_date,
                "endDate": end_date
            }
        }
        
        result = await call_garmin("query_garmin_graphql", query)

        if not result or "data" not in result:
            return "No scheduled workouts found or error querying data."

        scheduled = result.get("data", {}).get("workoutScheduleSummariesScalar", [])

        if not scheduled:
            return f"No workouts scheduled between {start_date} and {end_date}."

        return serialize_response(scheduled)

    @app.tool()
    @handle_garmin_errors
    async def get_training_plan_workouts(calendar_date: str) -> str:
        """Get training plan workouts for a specific date.

        Returns workouts from your active training plan scheduled for the given date.

        Args:
            calendar_date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with training plan data or error message
        """
        # Validate date (prevents GraphQL injection)
        calendar_date = validate_date(calendar_date, "calendar_date")
        
        # Use GraphQL variables to prevent injection (SECURITY FIX)
        query = {
            "query": """
                query($calendarDate: String!, $lang: String!, $firstDayOfWeek: String!) {
                    trainingPlanScalar(calendarDate: $calendarDate, lang: $lang, firstDayOfWeek: $firstDayOfWeek)
                }
            """,
            "variables": {
                "calendarDate": calendar_date,
                "lang": "en-US",
                "firstDayOfWeek": "monday"
            }
        }
        
        result = await call_garmin("query_garmin_graphql", query)

        if not result or "data" not in result:
            return "No training plan data found or error querying data."

        plan_data = result.get("data", {}).get("trainingPlanScalar", {})
        workouts = plan_data.get("trainingPlanWorkoutScheduleDTOS", [])

        if not workouts:
            return f"No training plan workouts scheduled for {calendar_date}."

        return serialize_response(plan_data)

    return app