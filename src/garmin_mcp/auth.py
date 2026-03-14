"""Authentication module for Garmin Connect.

Handles lazy authentication with OAuth token caching via garth (used internally
by garminconnect). Tokens are cached in ~/.garmin-mcp/ to avoid re-authentication
on every server restart.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from garminconnect import Garmin

load_dotenv()

logger = logging.getLogger("garmin_mcp.auth")

DEFAULT_TOKEN_DIR = Path.home() / ".garmin-mcp"

_garmin_instance: Garmin | None = None


def get_token_dir() -> Path:
    """Get the token cache directory from env or default."""
    token_dir = os.getenv("GARMIN_TOKEN_DIR")
    if token_dir:
        return Path(token_dir).expanduser()
    return DEFAULT_TOKEN_DIR


def authenticate() -> Garmin:
    """Authenticate with Garmin Connect, using cached tokens if available.

    Authentication flow:
    1. Try to load cached tokens from token dir
    2. If no cached tokens, authenticate with email/password
    3. Cache tokens for future use

    Returns:
        Authenticated Garmin instance.

    Raises:
        ValueError: If GARMIN_EMAIL or GARMIN_PASSWORD not set and no cached tokens.
        RuntimeError: If authentication fails.
    """
    global _garmin_instance

    if _garmin_instance is not None:
        return _garmin_instance

    token_dir = get_token_dir()

    # Try cached tokens first
    if token_dir.exists():
        try:
            garmin = Garmin()
            garmin.login(token_dir)
            logger.info("Authenticated using cached tokens from %s", token_dir)
            _garmin_instance = garmin
            return garmin
        except Exception:
            logger.info("Cached tokens expired or invalid, re-authenticating")

    # Fall back to email/password
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        raise ValueError(
            "GARMIN_EMAIL and GARMIN_PASSWORD environment variables are required "
            "when no cached tokens are available. Set them in .env or your MCP config."
        )

    try:
        garmin = Garmin(email, password, return_on_mfa=True)
        result = garmin.login()

        if isinstance(result, tuple) and result[0] == "needs_mfa":
            raise RuntimeError(
                "MFA is required but cannot be handled in server mode (stdin is reserved "
                "for MCP transport). Run 'uv run python scripts/setup_auth.py' first to "
                "cache tokens, then restart the server."
            )

        # Cache tokens
        token_dir.mkdir(parents=True, exist_ok=True)
        garmin.garth.dump(str(token_dir))
        logger.info("Authenticated and cached tokens to %s", token_dir)

        _garmin_instance = garmin
        return garmin
    except Exception as e:
        raise RuntimeError(f"Failed to authenticate with Garmin Connect: {e}") from e


def reset_auth() -> None:
    """Reset the cached authentication (useful for testing)."""
    global _garmin_instance
    _garmin_instance = None
