"""
Health & Wellness Data functions for Garmin Connect MCP Server
"""
import logging
from typing import Optional

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.validation import validate_date, validate_date_range

logger = logging.getLogger(__name__)

# The garmin_client will be set by the main file
garmin_client = None


def configure(client):
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client


def register_tools(app):
    """Register all health and wellness tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_stats(date: str) -> str:
        """Get daily activity stats
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with stats or error message
        """
        date = validate_date(date, "date")
        stats = garmin_client.get_stats(date)
        
        if not stats:
            return f"No stats found for {date}"
        
        return serialize_response(stats)

    @app.tool()
    @handle_garmin_errors
    async def get_user_summary(date: str) -> str:
        """Get user summary data (compatible with garminconnect-ha)
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with user summary or error message
        """
        date = validate_date(date, "date")
        summary = garmin_client.get_user_summary(date)
        
        if not summary:
            return f"No user summary found for {date}"
        
        return serialize_response(summary)

    @app.tool()
    @handle_garmin_errors
    async def get_body_composition(start_date: str, end_date: Optional[str] = None) -> str:
        """Get body composition data for a single date or date range
        
        Args:
            start_date: Date in YYYY-MM-DD format or start date if end_date provided
            end_date: Optional end date in YYYY-MM-DD format for date range
            
        Returns:
            JSON string with body composition data or error message
        """
        start_date = validate_date(start_date, "start_date")
        
        if end_date:
            start_date, end_date = validate_date_range(start_date, end_date)
            composition = garmin_client.get_body_composition(start_date, end_date)
            if not composition:
                return f"No body composition data found between {start_date} and {end_date}"
        else:
            composition = garmin_client.get_body_composition(start_date)
            if not composition:
                return f"No body composition data found for {start_date}"
        
        return serialize_response(composition)

    @app.tool()
    @handle_garmin_errors
    async def get_stats_and_body(date: str) -> str:
        """Get stats and body composition data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with stats and body composition data or error message
        """
        date = validate_date(date, "date")
        data = garmin_client.get_stats_and_body(date)
        
        if not data:
            return f"No stats and body composition data found for {date}"
        
        return serialize_response(data)

    @app.tool()
    @handle_garmin_errors
    async def get_steps_data(date: str) -> str:
        """Get steps data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with steps data or error message
        """
        date = validate_date(date, "date")
        steps_data = garmin_client.get_steps_data(date)
        
        if not steps_data:
            return f"No steps data found for {date}"
        
        return serialize_response(steps_data)

    @app.tool()
    @handle_garmin_errors
    async def get_daily_steps(start_date: str, end_date: str) -> str:
        """Get steps data for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with daily steps data or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        steps_data = garmin_client.get_daily_steps(start_date, end_date)
        
        if not steps_data:
            return f"No daily steps data found between {start_date} and {end_date}"
        
        return serialize_response(steps_data)

    @app.tool()
    @handle_garmin_errors
    async def get_training_readiness(date: str) -> str:
        """Get training readiness data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with training readiness data or error message
        """
        date = validate_date(date, "date")
        readiness = garmin_client.get_training_readiness(date)
        
        if not readiness:
            return f"No training readiness data found for {date}"
        
        return serialize_response(readiness)

    @app.tool()
    @handle_garmin_errors
    async def get_body_battery(start_date: str, end_date: str) -> str:
        """Get body battery data
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with body battery data or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        battery_data = garmin_client.get_body_battery(start_date, end_date)
        
        if not battery_data:
            return f"No body battery data found between {start_date} and {end_date}"
        
        return serialize_response(battery_data)

    @app.tool()
    @handle_garmin_errors
    async def get_body_battery_events(date: str) -> str:
        """Get body battery events data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with body battery events or error message
        """
        date = validate_date(date, "date")
        events = garmin_client.get_body_battery_events(date)
        
        if not events:
            return f"No body battery events found for {date}"
        
        return serialize_response(events)

    @app.tool()
    @handle_garmin_errors
    async def get_blood_pressure(start_date: str, end_date: str) -> str:
        """Get blood pressure data
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with blood pressure data or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)
        bp_data = garmin_client.get_blood_pressure(start_date, end_date)
        
        if not bp_data:
            return f"No blood pressure data found between {start_date} and {end_date}"
        
        return serialize_response(bp_data)

    @app.tool()
    @handle_garmin_errors
    async def get_floors(date: str) -> str:
        """Get floors climbed data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with floors data or error message
        """
        date = validate_date(date, "date")
        floors_data = garmin_client.get_floors(date)
        
        if not floors_data:
            return f"No floors data found for {date}"
        
        return serialize_response(floors_data)

    @app.tool()
    @handle_garmin_errors
    async def get_training_status(date: str) -> str:
        """Get training status data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with training status data or error message
        """
        date = validate_date(date, "date")
        status = garmin_client.get_training_status(date)
        
        if not status:
            return f"No training status data found for {date}"
        
        return serialize_response(status)

    @app.tool()
    @handle_garmin_errors
    async def get_rhr_day(date: str) -> str:
        """Get resting heart rate data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with resting heart rate data or error message
        """
        date = validate_date(date, "date")
        rhr_data = garmin_client.get_rhr_day(date)
        
        if not rhr_data:
            return f"No resting heart rate data found for {date}"
        
        return serialize_response(rhr_data)

    @app.tool()
    @handle_garmin_errors
    async def get_heart_rates(date: str) -> str:
        """Get heart rate data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with heart rate data or error message
        """
        date = validate_date(date, "date")
        hr_data = garmin_client.get_heart_rates(date)
        
        if not hr_data:
            return f"No heart rate data found for {date}"
        
        return serialize_response(hr_data)

    @app.tool()
    @handle_garmin_errors
    async def get_hydration_data(date: str) -> str:
        """Get hydration data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with hydration data or error message
        """
        date = validate_date(date, "date")
        hydration_data = garmin_client.get_hydration_data(date)
        
        if not hydration_data:
            return f"No hydration data found for {date}"
        
        return serialize_response(hydration_data)

    @app.tool()
    @handle_garmin_errors
    async def get_sleep_data(date: str) -> str:
        """Get sleep data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with sleep data or error message
        """
        date = validate_date(date, "date")
        sleep_data = garmin_client.get_sleep_data(date)
        
        if not sleep_data:
            return f"No sleep data found for {date}"
        
        return serialize_response(sleep_data)

    @app.tool()
    @handle_garmin_errors
    async def get_stress_data(date: str) -> str:
        """Get stress data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with stress data or error message
        """
        date = validate_date(date, "date")
        stress_data = garmin_client.get_stress_data(date)
        
        if not stress_data:
            return f"No stress data found for {date}"
        
        return serialize_response(stress_data)

    @app.tool()
    @handle_garmin_errors
    async def get_respiration_data(date: str) -> str:
        """Get respiration data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with respiration data or error message
        """
        date = validate_date(date, "date")
        respiration_data = garmin_client.get_respiration_data(date)
        
        if not respiration_data:
            return f"No respiration data found for {date}"
        
        return serialize_response(respiration_data)

    @app.tool()
    @handle_garmin_errors
    async def get_spo2_data(date: str) -> str:
        """Get SpO2 (blood oxygen) data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with SpO2 data or error message
        """
        date = validate_date(date, "date")
        spo2_data = garmin_client.get_spo2_data(date)
        
        if not spo2_data:
            return f"No SpO2 data found for {date}"
        
        return serialize_response(spo2_data)

    @app.tool()
    @handle_garmin_errors
    async def get_all_day_stress(date: str) -> str:
        """Get all-day stress data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with all-day stress data or error message
        """
        date = validate_date(date, "date")
        stress_data = garmin_client.get_all_day_stress(date)
        
        if not stress_data:
            return f"No all-day stress data found for {date}"
        
        return serialize_response(stress_data)

    @app.tool()
    @handle_garmin_errors
    async def get_all_day_events(date: str) -> str:
        """Get daily wellness events data
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with daily wellness events or error message
        """
        date = validate_date(date, "date")
        events = garmin_client.get_all_day_events(date)
        
        if not events:
            return f"No daily wellness events found for {date}"
        
        return serialize_response(events)

    return app
