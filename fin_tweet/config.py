import json
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "bearer_token": "",
        "csrf_token": "",
        "cookies": "",
        "user_id": "",
        "user_agent": "Mozilla/5.0",
        "x_twitter_auth_type": "OAuth2Session",
        "x_twitter_active_user": "yes",
        "x_twitter_client_language": "en",
        "accept_language": "en-US,en;q=0.9",
    }


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to JSON file."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
