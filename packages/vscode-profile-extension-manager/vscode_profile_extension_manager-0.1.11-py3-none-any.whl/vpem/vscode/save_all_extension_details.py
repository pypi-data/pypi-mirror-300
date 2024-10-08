from typing import Dict

from .extension_details import VscodeExtensionDetails
from .. import ALL_EXTENSION_DETAILS


def save_all_extension_details(all: Dict[str, VscodeExtensionDetails]):
    import json

    with open(ALL_EXTENSION_DETAILS, "w") as f:
        json.dump(all, f, indent=2)
    print(f"Extension details have been written to {ALL_EXTENSION_DETAILS}")
