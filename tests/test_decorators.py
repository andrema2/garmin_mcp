import pytest

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.errors import GarminValidationError


@pytest.mark.anyio
async def test_handle_garmin_errors_catches_custom_exception():
    @handle_garmin_errors
    async def tool():
        raise GarminValidationError("bad input")

    out = await tool()
    assert out == "Error: bad input"


@pytest.mark.anyio
async def test_handle_garmin_errors_serializes_non_string():
    @handle_garmin_errors
    async def tool():
        return {"ok": True}

    out = await tool()
    assert '"ok"' in out


@pytest.mark.anyio
async def test_handle_garmin_errors_supports_sync_tool():
    @handle_garmin_errors
    def tool():
        return {"sync": True}

    out = await tool()
    assert '"sync"' in out


