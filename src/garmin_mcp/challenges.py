"""
Challenges and badges functions for Garmin Connect MCP Server
"""
import logging

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import (
    validate_date_range,
    validate_positive_number,
    sanitize_string,
)

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all challenges-related tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def get_goals(goal_type: str = "active") -> str:
        """Get Garmin Connect goals (active, future, or past)

        Args:
            goal_type: Type of goals to retrieve. Options: "active", "future", or "past"
            
        Returns:
            JSON string with goals or error message
        """
        goal_type = sanitize_string(goal_type, "goal_type")
        
        if goal_type not in ("active", "future", "past"):
            raise ValueError(f"goal_type must be 'active', 'future', or 'past', got '{goal_type}'")

        goals = await call_garmin("get_goals", goal_type)
        if not goals:
            return f"No {goal_type} goals found."
        return serialize_response(goals)

    @app.tool()
    @handle_garmin_errors
    async def get_personal_record() -> str:
        """Get personal records for user
        
        Returns:
            JSON string with personal records or error message
        """
        records = await call_garmin("get_personal_record")
        if not records:
            return "No personal records found."
        return serialize_response(records)

    @app.tool()
    @handle_garmin_errors
    async def get_earned_badges() -> str:
        """Get earned badges for user
        
        Returns:
            JSON string with earned badges or error message
        """
        badges = await call_garmin("get_earned_badges")
        if not badges:
            return "No earned badges found."
        return serialize_response(badges)

    @app.tool()
    @handle_garmin_errors
    async def get_adhoc_challenges(start: int = 0, limit: int = 100) -> str:
        """Get adhoc challenges data

        Args:
            start: Starting index for challenges retrieval (must be >= 0)
            limit: Maximum number of challenges to retrieve (must be positive)
            
        Returns:
            JSON string with challenges or error message
        """
        start = int(validate_positive_number(start, "start", allow_zero=True))
        limit = int(validate_positive_number(limit, "limit", allow_zero=False))

        challenges = await call_garmin("get_adhoc_challenges", start, limit)
        if not challenges:
            return "No adhoc challenges found."
        return serialize_response(challenges)

    @app.tool()
    @handle_garmin_errors
    async def get_available_badge_challenges(start: int = 1, limit: int = 100) -> str:
        """Get available badge challenges data

        Args:
            start: Starting index for challenges retrieval (starts at 1, must be positive)
            limit: Maximum number of challenges to retrieve (must be positive)
            
        Returns:
            JSON string with challenges or error message
        """
        start = int(validate_positive_number(start, "start", allow_zero=False))
        limit = int(validate_positive_number(limit, "limit", allow_zero=False))

        challenges = await call_garmin("get_available_badge_challenges", start, limit)
        if not challenges:
            return "No available badge challenges found."
        return serialize_response(challenges)

    @app.tool()
    @handle_garmin_errors
    async def get_badge_challenges(start: int = 1, limit: int = 100) -> str:
        """Get badge challenges data

        Args:
            start: Starting index for challenges retrieval (starts at 1, must be positive)
            limit: Maximum number of challenges to retrieve (must be positive)
            
        Returns:
            JSON string with challenges or error message
        """
        start = int(validate_positive_number(start, "start", allow_zero=False))
        limit = int(validate_positive_number(limit, "limit", allow_zero=False))

        challenges = await call_garmin("get_badge_challenges", start, limit)
        if not challenges:
            return "No badge challenges found."
        return serialize_response(challenges)

    @app.tool()
    @handle_garmin_errors
    async def get_non_completed_badge_challenges(start: int = 1, limit: int = 100) -> str:
        """Get non-completed badge challenges data

        Args:
            start: Starting index for challenges retrieval (starts at 1, must be positive)
            limit: Maximum number of challenges to retrieve (must be positive)
            
        Returns:
            JSON string with challenges or error message
        """
        start = int(validate_positive_number(start, "start", allow_zero=False))
        limit = int(validate_positive_number(limit, "limit", allow_zero=False))

        challenges = await call_garmin("get_non_completed_badge_challenges", start, limit)
        if not challenges:
            return "No non-completed badge challenges found."
        return serialize_response(challenges)

    @app.tool()
    @handle_garmin_errors
    async def get_race_predictions() -> str:
        """Get race predictions for user
        
        Returns:
            JSON string with race predictions or error message
        """
        predictions = await call_garmin("get_race_predictions")
        if not predictions:
            return "No race predictions found."
        return serialize_response(predictions)

    @app.tool()
    @handle_garmin_errors
    async def get_inprogress_virtual_challenges(start_date: str, end_date: str) -> str:
        """Get in-progress virtual challenges/expeditions between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            JSON string with challenges or error message
        """
        start_date, end_date = validate_date_range(start_date, end_date)

        challenges = await call_garmin("get_inprogress_virtual_challenges", start_date, end_date)
        if not challenges:
            return f"No in-progress virtual challenges found between {start_date} and {end_date}."
        return serialize_response(challenges)

    return app
