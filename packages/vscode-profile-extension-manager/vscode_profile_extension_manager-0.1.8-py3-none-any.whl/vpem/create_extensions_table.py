from vpem.vscode.extension_details import VscodeExtensionDetails


from rich.table import Table
from rich.console import Console


from datetime import datetime
from typing import Dict, List


console = Console()


def create_extensions_table(
    todo: List[str],
    extensions_data: Dict[str, VscodeExtensionDetails],
    title="VS Code Extensions to be categorized",
):
    todo_data = {ext_id: extensions_data[ext_id] for ext_id in todo}

    table = Table(title=title)

    table.add_column("Extension ID", style="cyan", no_wrap=True)
    table.add_column("Extension Name", style="magenta", width=50)
    table.add_column("Last Updated", style="magenta")
    table.add_column("Description", style="green")

    for ext_info in todo_data.values():
        last_updated = "-unknown-"
        if "lastUpdated" in ext_info:
            try:
                last_updated = datetime.fromisoformat(ext_info.lastUpdated).strftime(
                    "%B %d, %Y"
                )
            except ValueError:
                last_updated = "-unknown-"
        table.add_row(
            ext_info.extensionName,
            ext_info.displayName,
            last_updated,
            ext_info.shortDescription,
        )

    console.print(table)
