"""
Device-related functions for Garmin Connect MCP Server
"""
import logging
from typing import Optional

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import validate_date, resolve_date, sanitize_string

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all device-related tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_devices() -> str:
        """Get all Garmin devices associated with the user account
        
        Returns:
            JSON string with devices or error message
        """
        devices = await call_garmin("get_devices")
        if not devices:
            return "No devices found."
        return serialize_response(devices)

    @app.tool()
    @handle_garmin_errors
    async def get_device_last_used() -> str:
        """Get information about the last used Garmin device
        
        Returns:
            JSON string with device information or error message
        """
        device = await call_garmin("get_device_last_used")
        if not device:
            return "No last used device found."
        return serialize_response(device)
    
    @app.tool()
    @handle_garmin_errors
    async def get_device_settings(device_id: str) -> str:
        """Get settings for a specific Garmin device
        
        Args:
            device_id: Device ID (will be sanitized)
            
        Returns:
            JSON string with device settings or error message
        """
        device_id = sanitize_string(device_id, "device_id")
        settings = await call_garmin("get_device_settings", device_id)
        if not settings:
            return f"No settings found for device ID {device_id}."
        return serialize_response(settings)

    @app.tool()
    @handle_garmin_errors
    async def get_primary_training_device() -> str:
        """Get information about the primary training device
        
        Returns:
            JSON string with device information or error message
        """
        device = await call_garmin("get_primary_training_device")
        if not device:
            return "No primary training device found."
        return serialize_response(device)
    
    @app.tool()
    @handle_garmin_errors
    async def get_device_solar_data(device_id: str, date: Optional[str] = None) -> str:
        """Get solar data for a specific device
        
        Args:
            device_id: Device ID (will be sanitized)
            date: Date in YYYY-MM-DD format
            
        Returns:
            JSON string with solar data or error message
        """
        device_id = sanitize_string(device_id, "device_id")
        date = resolve_date(date, "date")
        solar_data = await call_garmin("get_device_solar_data", device_id, date)
        if not solar_data:
            return f"No solar data found for device ID {device_id} on {date}."
        return serialize_response(solar_data)
    
    @app.tool()
    @handle_garmin_errors
    async def get_device_alarms() -> str:
        """Get alarms from all Garmin devices
        
        Returns:
            JSON string with device alarms or error message
        """
        alarms = await call_garmin("get_device_alarms")
        if not alarms:
            return "No device alarms found."
        return serialize_response(alarms)

    return app
