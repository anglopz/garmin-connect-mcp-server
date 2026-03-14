"""Smoke tests for GarminClient initialization."""

from garmin_mcp.client import GarminClient


def test_client_init(mock_garmin):
    """Client initializes with a Garmin instance."""
    client = GarminClient(mock_garmin)
    assert client._garmin is mock_garmin
