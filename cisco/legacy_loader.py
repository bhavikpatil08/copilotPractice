import json
from typing import List, Dict, Any


def load_users(file_path: str) -> List[Dict[str, Any]]:
    """
    Load users from a JSON file and return only active users.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            users = json.load(file)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File '{file_path}' not found") from exc

    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON format in '{file_path}'") from exc

    except OSError as exc:
        raise OSError(f"Error reading file '{file_path}'") from exc

    if not isinstance(users, list):
        raise ValueError("JSON data must be a list of users")

    # Return only active users
    return [user for user in users if user.get("active") is True]