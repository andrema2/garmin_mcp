"""
Modular MCP Server for Garmin Connect Data
"""

import os
import sys
import logging
import threading

import requests  # type: ignore
from mcp.server.fastmcp import FastMCP  # type: ignore

from garth.exc import GarthHTTPError  # type: ignore
from garminconnect import Garmin, GarminConnectAuthenticationError  # type: ignore

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.validation import validate_positive_number

# Import all modules
from garmin_mcp import activity_management
from garmin_mcp import health_wellness
from garmin_mcp import user_profile
from garmin_mcp import devices
from garmin_mcp import gear_management
from garmin_mcp import weight_management
from garmin_mcp import challenges
from garmin_mcp import training
from garmin_mcp import workouts
from garmin_mcp import data_management
from garmin_mcp import womens_health

# Configurar logging para stderr (não interfere no protocolo MCP)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)

# Global Garmin client with lazy initialization (thread-safe)
_garmin_client = None
_garmin_client_lock = threading.Lock()


def get_mfa() -> str:
    """Get MFA code from environment variable
    
    Cannot use interactive input() in MCP server mode as stdin is used
    for the MCP protocol communication.
    """
    mfa_code = os.environ.get("GARMIN_MFA_CODE")
    if not mfa_code:
        logger.error(
            "MFA code required but GARMIN_MFA_CODE environment variable not set. "
            "Cannot use interactive input in MCP server mode (stdin is used for protocol)."
        )
        raise ValueError(
            "MFA code required. Set GARMIN_MFA_CODE environment variable. "
            "Interactive input is not available in MCP server mode."
        )
    logger.info("MFA code retrieved from environment variable")
    return mfa_code


def read_credential_file(file_path: str, credential_type: str) -> str:
    """Read credential from file with proper error handling
    
    Args:
        file_path: Path to the credential file
        credential_type: Type of credential (for error messages)
        
    Returns:
        Credential string from file
        
    Raises:
        ValueError: If file cannot be read or is empty
    """
    try:
        expanded_path = os.path.expanduser(file_path)
        if not os.path.exists(expanded_path):
            raise ValueError(
                f"{credential_type} file not found: {expanded_path}"
            )
        
        if not os.access(expanded_path, os.R_OK):
            raise ValueError(
                f"Permission denied reading {credential_type} file: {expanded_path}"
            )
        
        with open(expanded_path, "r", encoding="utf-8") as f:
            content = f.read().rstrip()
        
        if not content:
            raise ValueError(
                f"{credential_type} file is empty: {expanded_path}"
            )
        
        return content
        
    except OSError as e:
        raise ValueError(
            f"Error reading {credential_type} file {file_path}: {str(e)}"
        ) from e


def _get_credentials():
    """Get credentials from environment (lazy loading)
    
    Returns:
        Tuple of (email, password)
    """
    email = os.environ.get("GARMIN_EMAIL")
    email_file_path = os.environ.get("GARMIN_EMAIL_FILE")
    if email and email_file_path:
        raise ValueError(
            "Must only provide one of GARMIN_EMAIL and GARMIN_EMAIL_FILE, got both"
        )
    elif email_file_path:
        email = read_credential_file(email_file_path, "Email")

    password = os.environ.get("GARMIN_PASSWORD")
    password_file_path = os.environ.get("GARMIN_PASSWORD_FILE")
    if password and password_file_path:
        raise ValueError(
            "Must only provide one of GARMIN_PASSWORD and GARMIN_PASSWORD_FILE, got both"
        )
    elif password_file_path:
        password = read_credential_file(password_file_path, "Password")
    
    return email, password


# Expand paths for token storage (critical fix)
tokenstore = os.path.expanduser(os.getenv("GARMINTOKENS") or "~/.garminconnect")
tokenstore_base64 = os.path.expanduser(
    os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"
)


def init_api(email, password):
    """Initialize Garmin API with your credentials."""
    try:
        # Using Oauth1 and OAuth2 token files from directory
        logger.info(f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...")

        garmin = Garmin()
        garmin.login(tokenstore)
        logger.info("Successfully logged in using stored tokens")

    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        logger.info(
            "Login tokens not present or expired, login with your Garmin Connect credentials to generate them. "
            f"They will be stored in '{tokenstore}' for future use."
        )
        try:
            if not email or not password:
                logger.error("Email and password required for initial login but not provided")
                return None
                
            garmin = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            garmin.login()
            # Save Oauth1 and OAuth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            logger.info(f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)")
            
            # Encode Oauth1 and Oauth2 tokens to base64 string and save to file for next login (alternative way)
            token_base64 = garmin.garth.dumps()
            dir_path = os.path.expanduser(tokenstore_base64)
            with open(dir_path, "w") as token_file:
                token_file.write(token_base64)
            logger.info(f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)")
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error(f"Failed to login: {err}", exc_info=True)
            return None

    return garmin


def get_garmin_client():
    """Get Garmin client with lazy initialization (thread-safe)
    
    This function initializes the Garmin client on first call, making the
    MCP server start instantly without waiting for authentication.
    
    Returns:
        Garmin client instance
        
    Raises:
        RuntimeError: If client initialization fails
    """
    global _garmin_client
    
    # Fast path: client already initialized
    if _garmin_client is not None:
        return _garmin_client
    
    # Thread-safe initialization
    with _garmin_client_lock:
        # Double-check pattern
        if _garmin_client is not None:
            return _garmin_client
        
        logger.info("Lazy initializing Garmin Connect client...")
        email, password = _get_credentials()
        client = init_api(email, password)
        
        if not client:
            raise RuntimeError(
                "Failed to initialize Garmin Connect client. "
                "Please check your credentials and try again."
            )
        
        _garmin_client = client
        logger.info("Garmin Connect client initialized successfully (lazy init).")
        return _garmin_client


def main():
    """Initialize the MCP server and register all tools
    
    Note: Garmin client initialization is deferred until first tool call
    to allow MCP server to start instantly.
    """
    # Create the MCP app FIRST (before any blocking operations)
    app = FastMCP("Garmin Connect v1.0")

    # Register tools from all modules (no client initialization yet)
    app = activity_management.register_tools(app)
    app = health_wellness.register_tools(app)
    app = user_profile.register_tools(app)
    app = devices.register_tools(app)
    app = gear_management.register_tools(app)
    app = weight_management.register_tools(app)
    app = challenges.register_tools(app)
    app = training.register_tools(app)
    app = workouts.register_tools(app)
    app = data_management.register_tools(app)
    app = womens_health.register_tools(app)

    # Add activity listing tool directly to the app
    @app.tool()
    @handle_garmin_errors
    async def list_activities(limit: int = 5) -> str:
        """List recent Garmin activities
        
        Args:
            limit: Maximum number of activities to retrieve (default: 5, must be positive)
            
        Returns:
            Formatted string with activity information
        """
        # Lazy init client on first use
        garmin_client = get_garmin_client()
        
        # Validate limit
        limit = int(validate_positive_number(limit, "limit", allow_zero=False))
        
        activities = garmin_client.get_activities(0, limit)

        if not activities:
            return "No activities found."

        result = f"Last {len(activities)} activities:\n\n"
        for idx, activity in enumerate(activities, 1):
            result += f"--- Activity {idx} ---\n"
            result += f"Activity: {activity.get('activityName', 'Unknown')}\n"
            result += (
                f"Type: {activity.get('activityType', {}).get('typeKey', 'Unknown')}\n"
            )
            result += f"Date: {activity.get('startTimeLocal', 'Unknown')}\n"
            result += f"ID: {activity.get('activityId', 'Unknown')}\n\n"

        return result

    # Run the MCP server (starts instantly, no blocking operations)
    logger.info("Starting MCP server (Garmin client will initialize on first tool call)...")
    app.run()


if __name__ == "__main__":
    main()
