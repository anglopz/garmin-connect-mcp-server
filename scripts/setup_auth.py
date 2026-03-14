#!/usr/bin/env python3
"""Interactive authentication setup for Garmin Connect.

Checks for existing cached tokens and, if missing or expired,
prompts for credentials and caches new tokens via garth.
"""

import getpass
import sys
from pathlib import Path

from garminconnect import Garmin

DEFAULT_TOKEN_DIR = Path.home() / ".garmin-mcp"


def get_token_dir() -> Path:
    import os

    token_dir = os.getenv("GARMIN_TOKEN_DIR")
    if token_dir:
        return Path(token_dir).expanduser()
    return DEFAULT_TOKEN_DIR


def main() -> None:
    token_dir = get_token_dir()

    # Try existing cached tokens
    if token_dir.exists():
        try:
            garmin = Garmin()
            garmin.login(token_dir)
            print(f"Authenticated using cached tokens from {token_dir}")
            print("Token cache is valid -- no action needed.")
            return
        except Exception:
            print(f"Cached tokens in {token_dir} are expired or invalid.")

    # Prompt for credentials
    print("Garmin Connect authentication setup")
    print("------------------------------------")
    email = input("Email: ").strip()
    if not email:
        print("Error: email is required.", file=sys.stderr)
        sys.exit(1)

    password = getpass.getpass("Password: ")
    if not password:
        print("Error: password is required.", file=sys.stderr)
        sys.exit(1)

    try:
        garmin = Garmin(email, password, return_on_mfa=True)
        result = garmin.login()

        if isinstance(result, tuple) and result[0] == "needs_mfa":
            mfa_code = input("MFA code (check your email/authenticator): ").strip()
            if not mfa_code:
                print("Error: MFA code is required.", file=sys.stderr)
                sys.exit(1)
            garmin.resume_login(result[1], mfa_code)

        token_dir.mkdir(parents=True, exist_ok=True)
        garmin.garth.dump(str(token_dir))
        print(f"\nAuthenticated and cached tokens to {token_dir}")
        print("You can now run the MCP server without providing credentials.")
    except Exception as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
