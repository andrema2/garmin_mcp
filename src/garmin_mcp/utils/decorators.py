"""
Decorators for error handling and logging
"""

import logging
import inspect
from functools import partial
from functools import wraps
from typing import Callable, Any

from garmin_mcp.utils.errors import GarminMCPError
from garmin_mcp.utils.serialization import serialize_response

logger = logging.getLogger(__name__)


def handle_garmin_errors(func: Callable) -> Callable:
    """Decorator to handle errors consistently across all tool functions
    
    This decorator:
    - Catches exceptions and logs them appropriately
    - Serializes responses consistently
    - Returns user-friendly error messages
    
    Usage:
        @app.tool()
        @handle_garmin_errors
        async def my_tool(param: str) -> str:
            result = garmin_client.get_something(param)
            return result  # Will be serialized automatically
    """
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            # Suporta tools async e sync.
            # Se for sync (ex.: por conveniência ou testes), roda em thread para
            # não bloquear o event loop.
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                import anyio  # type: ignore

                result = await anyio.to_thread.run_sync(partial(func, *args, **kwargs))
            
            # Serialize if not already a string
            if not isinstance(result, str):
                return serialize_response(result)
            
            return result
            
        except GarminMCPError as e:
            # Custom exceptions - log as warning, return user-friendly message
            logger.warning(f"Validation/API error in {func.__name__}: {e}")
            return f"Error: {str(e)}"
            
        except Exception as e:
            # Unexpected errors - log with full traceback
            logger.error(
                f"Unexpected error in {func.__name__}: {e}",
                exc_info=True
            )
            return f"Error in {func.__name__}: {str(e)}"
    
    return wrapper

