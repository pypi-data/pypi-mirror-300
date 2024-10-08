from typing import Dict

from .. import ALL_EXTENSION_DETAILS
from .extension_details import VscodeExtensionDetails


def load_all_extension_details() -> Dict[str, VscodeExtensionDetails]:
    import json

    raw = {}
    try:
        raw = json.load(open(ALL_EXTENSION_DETAILS))
    except FileNotFoundError:
        pass
    all = {k: VscodeExtensionDetails.from_dict(v) for k, v in raw.items()}
    return all
