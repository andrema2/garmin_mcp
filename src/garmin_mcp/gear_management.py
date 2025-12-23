"""
Gear management functions for Garmin Connect MCP Server
"""
import logging

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.validation import sanitize_string

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all gear management tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_gear(user_profile_id: str) -> str:
        """Get all gear registered with the user account
        
        Args:
            user_profile_id: User profile ID (can be obtained from get_device_last_used, will be sanitized)
            
        Returns:
            JSON string with gear information or error message
        """
        from garmin_mcp import get_garmin_client
        garmin_client = get_garmin_client()
        
        user_profile_id = sanitize_string(user_profile_id, "user_profile_id")
        gear = garmin_client.get_gear(user_profile_id)
        if not gear:
            return "No gear found."
        return serialize_response(gear)

    @app.tool()
    @handle_garmin_errors
    async def get_gear_defaults(user_profile_id: str) -> str:
        """Get default gear settings
        
        Args:
            user_profile_id: User profile ID (can be obtained from get_device_last_used, will be sanitized)
            
        Returns:
            JSON string with gear defaults or error message
        """
        from garmin_mcp import get_garmin_client
        garmin_client = get_garmin_client()
        
        user_profile_id = sanitize_string(user_profile_id, "user_profile_id")
        defaults = garmin_client.get_gear_defaults(user_profile_id)
        if not defaults:
            return "No gear defaults found."
        return serialize_response(defaults)
    
    @app.tool()
    @handle_garmin_errors
    async def get_gear_stats(gear_uuid: str) -> str:
        """Get statistics for specific gear
        
        Args:
            gear_uuid: UUID of the gear item (will be sanitized)
            
        Returns:
            JSON string with gear statistics or error message
        """
        from garmin_mcp import get_garmin_client
        garmin_client = get_garmin_client()
        
        gear_uuid = sanitize_string(gear_uuid, "gear_uuid")
        stats = garmin_client.get_gear_stats(gear_uuid)
        if not stats:
            return f"No stats found for gear with UUID {gear_uuid}."
        return serialize_response(stats)

    return app
