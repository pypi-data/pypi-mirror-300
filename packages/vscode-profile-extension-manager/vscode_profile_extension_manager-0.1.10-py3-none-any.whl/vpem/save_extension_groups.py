import json
from typing import Dict, List
from . import EXTENSION_GROUPS


def save_extension_groups(groups: Dict[str, List[str]]) -> None:
    """Save the extension groups to the JSON file."""
    with open(EXTENSION_GROUPS, "w") as f:
        json.dump(groups, f, indent=2)
