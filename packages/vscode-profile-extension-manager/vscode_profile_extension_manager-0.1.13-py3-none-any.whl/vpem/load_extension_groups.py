import json
from typing import List, Dict
from . import EXTENSION_GROUPS


def load_extension_groups() -> Dict[str, List[str]]:
    """Load the extension groups from the JSON file."""
    try:
        with open(EXTENSION_GROUPS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
