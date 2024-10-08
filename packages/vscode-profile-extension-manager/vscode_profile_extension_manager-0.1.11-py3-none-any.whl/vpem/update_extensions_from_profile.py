import os

from .vscode.retrieve_vscode_ext_details import retrieve_vscode_ext_details
from .vscode.extension_details import VscodeExtensionDetails
from .vscode.load_all_extension_details import load_all_extension_details
from .vscode.save_all_extension_details import save_all_extension_details
from .vscode.list_installed_vscode_extensions import (
    list_installed_vscode_extensions,
)
from .result_with_err import ResultWithErr, OK, ERR
from rich.progress import Progress
from . import CONFIG_DIR


def update_extensions_from_profile(profile: str) -> ResultWithErr[None]:
    import json

    def add_profile(profile: str, current: dict):
        current.setdefault("profiles", []).append(profile)
        current["profiles"] = sorted(set(current["profiles"]))

    all = load_all_extension_details()

    print(f"Processing profile: {profile}")
    raw_profile_exts = os.path.join(CONFIG_DIR, f"vscode-extensions-{profile}.json")
    extensions, err = list_installed_vscode_extensions(profile)
    if err:
        return ERR(err)
    if not extensions:
        return ERR(Exception(f"No extensions found for profile {profile}"))

    # Write sorted extensions to input file
    json.dump(extensions, open(raw_profile_exts, "w"), indent=2)

    # Process extensions and write to output file
    all_exts = set(all.keys())
    profile_exts = set(extensions)
    new_exts = profile_exts - all_exts
    for k, v in all.items():
        if v.needs_refresh:
            new_exts.add(k)

    # remove profile for all extensions
    for extension in all_exts:
        if profile in all[extension].get("profiles", []):
            all[extension]["profiles"].remove(profile)

    # Update existing extensions
    for extension in profile_exts:
        current = all.get(extension, {})
        add_profile(profile, current)
        all[extension] = VscodeExtensionDetails.from_dict(current)

    # retrieve missing extensions
    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Retrieving extension details...", total=len(new_exts)
        )
        for extension in new_exts:
            details, err = retrieve_vscode_ext_details(extension)
            if err:
                print(f"Error: {err}")
                progress.advance(task)
                continue
            if not details:
                print(f"No details found for extension: {extension}")
                progress.advance(task)
                continue
            current = VscodeExtensionDetails.from_dict(details)
            assert current
            add_profile(profile, current)
            all[extension] = current
            progress.advance(task)

    save_all_extension_details(all)
    return OK(None)


if __name__ == "__main__":
    update_extensions_from_profile("Default")
