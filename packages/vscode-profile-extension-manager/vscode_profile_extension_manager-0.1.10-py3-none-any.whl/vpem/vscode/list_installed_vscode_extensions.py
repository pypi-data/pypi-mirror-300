import subprocess
from typing import List
from ..result_with_err import ResultWithErr, OK, ERR


def list_installed_vscode_extensions(profile: str) -> ResultWithErr[List[str]]:
    """
    Dumps the list of installed Visual Studio Code extensions for the specified profile.

    Args:
        profile (str): The name of the Visual Studio Code profile to get the extensions for.

    Returns:
        ResultWithErr[List[str]]: A result object containing the list of extension names, or an error if the operation failed.
    """

    try:
        result = subprocess.run(
            ["code", "--profile", profile, "--list-extensions"],
            capture_output=True,
            text=True,
            check=True,
        )
        extensions = [x for x in sorted(result.stdout.strip().split("\n")) if x]
        return OK(extensions)
    except subprocess.CalledProcessError as e:
        return ERR(Exception(f"Failed to get extensions for profile {profile}: {e}"))
    except Exception as e:
        return ERR(
            Exception(
                f"Unexpected error while getting extensions for profile {profile}: {e}"
            )
        )
