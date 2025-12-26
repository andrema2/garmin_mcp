"""
User Profile functions for Garmin Connect MCP Server
"""
import logging

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all user profile tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_full_name() -> str:
        """Get user's full name from profile
        
        Returns:
            User's full name or error message
        """
        full_name = await call_garmin("get_full_name")
        return full_name if isinstance(full_name, str) else serialize_response(full_name)

    @app.tool()
    @handle_garmin_errors
    async def get_unit_system() -> str:
        """Get user's preferred unit system from profile
        
        Returns:
            Unit system or error message
        """
        unit_system = await call_garmin("get_unit_system")
        return unit_system if isinstance(unit_system, str) else serialize_response(unit_system)
    
    @app.tool()
    @handle_garmin_errors
    async def get_user_profile() -> str:
        """Get user profile information
        
        Returns:
            JSON string with user profile information or error message
        """
        profile = await call_garmin("get_user_profile")
        if not profile:
            return "No user profile information found."
        return serialize_response(profile)

    @app.tool()
    @handle_garmin_errors
    async def get_userprofile_settings() -> str:
        """Get user profile settings
        
        Returns:
            JSON string with user profile settings or error message
        """
        settings = await call_garmin("get_userprofile_settings")
        if not settings:
            return "No user profile settings found."
        return serialize_response(settings)

    return app
