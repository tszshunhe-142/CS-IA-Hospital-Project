"""Create MySQL connections using environment-based settings."""

import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# Resolve from this file so configuration works from any PowerShell directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=True)


def get_connection():
    """Open a connection using DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD."""
    required_settings = ("DB_NAME", "DB_USER", "DB_PASSWORD")
    missing_settings = [name for name in required_settings if not os.environ.get(name)]
    if missing_settings:
        raise ValueError("Missing MySQL settings: " + ", ".join(missing_settings))

    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
