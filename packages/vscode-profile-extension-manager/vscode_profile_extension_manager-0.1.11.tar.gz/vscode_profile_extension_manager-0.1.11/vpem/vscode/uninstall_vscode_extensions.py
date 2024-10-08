import subprocess
from typing import List
from ..result_with_err import ResultWithErr, OK, ERR


def uninstall_vscode_extension(profile: str, extension_id: str) -> ResultWithErr[None]:
    """
    Uninstalls a Visual Studio Code extension for the specified profile.

    Args:
        profile (str): The profile to install the extension for.
        extension_id (str): The ID of the extension to uninstall.

    Returns:
        ResultWithErr[None]: A result object indicating whether the installation was successful or not.
    """
    try:
        results = subprocess.run(
            ["code", "--profile", profile, "--uninstall-extension", extension_id],
            capture_output=True,
            text=True,
            check=True,
        )
        return OK(None)
    except subprocess.CalledProcessError as e:
        return ERR(
            Exception(f"Failed to uninstall extensions for profile {profile}: {e}")
        )
    except Exception as e:
        return ERR(
            Exception(
                f"Unexpected error while uninstalling extensions for profile {profile}: {e}"
            )
        )
