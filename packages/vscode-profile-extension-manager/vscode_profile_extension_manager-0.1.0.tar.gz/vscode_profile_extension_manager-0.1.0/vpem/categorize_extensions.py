import json
import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Union
from rich.console import Console
from rich.prompt import Prompt
import inquirer

from .create_extensions_table import create_extensions_table

from .vscode.extension_details import VscodeExtensionDetails

from .load_extension_groups import load_extension_groups
from .save_extension_groups import save_extension_groups
from .vscode.load_all_extension_details import load_all_extension_details


console = Console()


def build_todo(uncategorized_only=True) -> List[str]:
    all = load_all_extension_details()
    groups = load_extension_groups()
    grouped_keys = set()
    for group_extensions in groups.values():
        grouped_keys.update(group_extensions)

    # Remove items from 'all' that have keys from singles
    if uncategorized_only:
        todo = [ext_id for ext_id in all.keys() if ext_id not in grouped_keys]
    else:
        todo = list(all.keys())

    return todo


class SearchCondition(Enum):
    QUIT = ":q"
    DEFAULT = ":d"
    REMOVE = ":r"
    FILTER = "search_string"


def filter_extensions(
    todo: List[str], extensions_data: Dict[str, VscodeExtensionDetails]
) -> Tuple[List[str], SearchCondition]:
    done = len(todo) == 0
    filtered_extensions = []
    sc = SearchCondition.QUIT
    if not done:
        console.print(
            f"""
This is a list of extensions that have not yet been categorized. Enter a regular expression to filter the list.  
Other shortcuts:
    :q - [bold]Q[/bold]uit
    :d - Set remaining to your [bold]D][/bold]efault extensions
    :r search_string - [bold]R[/bold]emove extensions matching search string from list (stored in 'removed' group)
    search_string - Filter extensions matching search string (can be regular expression) """
        )
    while not done:
        search_string = inquirer.text("Search", validate=lambda _, x: len(x) > 0)
        if search_string.lower() == ":q":
            return todo, SearchCondition.QUIT
        sc: SearchCondition = SearchCondition.FILTER
        if search_string.lower() == ":d":
            sc = SearchCondition.DEFAULT
            search_string = ".*"
        elif search_string.lower().startswith(":r"):
            sc = SearchCondition.REMOVE
            search_string = search_string[3:]

        todo_data = {ext_id: extensions_data[ext_id] for ext_id in todo}

        for ext_id, ext_info in todo_data.items():
            if (
                re.search(search_string, ext_id, re.IGNORECASE)
                or re.search(search_string, ext_info.displayName, re.IGNORECASE)
                or re.search(search_string, ext_info.shortDescription, re.IGNORECASE)
            ):
                filtered_extensions.append(ext_id)
        done = len(filtered_extensions) > 0

    return filtered_extensions, sc


def categorize_extensions(uncategorized_only=True):
    extensions_data = load_all_extension_details()
    done = False
    while not done:
        todo = build_todo(uncategorized_only)
        uncategorized_only = True  # only do this first time thru loop
        console.clear()
        create_extensions_table(todo, extensions_data)
        filtered_extensions, sc = filter_extensions(todo, extensions_data)

        if sc == SearchCondition.QUIT:
            break
        elif not filtered_extensions:
            continue
        elif sc == SearchCondition.DEFAULT:
            create_extensions_table(
                filtered_extensions,
                extensions_data,
                f"Default Extensions for all Profiles",
            )
            answer = inquirer.confirm(message="Make these the default?", default=True)
            if not answer:
                continue
            group_name = "Default"
        elif sc == SearchCondition.REMOVE:
            create_extensions_table(
                filtered_extensions,
                extensions_data,
                f"Extensions to remove",
            )
            answer = inquirer.confirm(
                message="Move these extensiosn to 'removed' group", default=True
            )
            if not answer:
                continue
            group_name = "removed"
        else:
            create_extensions_table(
                filtered_extensions,
                extensions_data,
                f"Extensions to add to group",
            )
            console.print(
                """    :r - redo search
Group Name (should start with a capital letter)""",
            )
            group_name = inquirer.text(
                "Group ", validate=lambda _, x: re.match(r"^:[r]|[A-Z][A-Za-z]{2}", x)
            )
            if group_name.startswith(":r"):
                continue
        groups = load_extension_groups()
        current = groups.get(group_name, [])
        groups[group_name] = list(set(current + list(filtered_extensions)))
        save_extension_groups(groups)
