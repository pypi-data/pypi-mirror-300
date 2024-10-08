import subprocess
from typing import List
from ..result_with_err import ResultWithErr, OK, ERR


def install_vscode_extension(profile: str, extension_id: str) -> ResultWithErr[None]:
    """
    Installs a Visual Studio Code extension for the specified profile.

    Args:
        profile (str): The profile to install the extension for.
        extension_id (str): The ID of the extension to install.

    Returns:
        ResultWithErr[None]: A result object indicating whether the installation was successful or not.
    """
    try:
        subprocess.run(
            ["code", "--profile", profile, "--install-extension", extension_id],
            capture_output=True,
            text=True,
            check=True,
        )
        return OK(None)
    except subprocess.CalledProcessError as e:
        return ERR(
            Exception(
                f"Failed to install extension {extension_id} for profile {profile}: {e}"
            )
        )
    except Exception as e:
        return ERR(
            Exception(
                f"Unexpected error while installing extension {extension_id} for profile {profile}: {e}"
            )
        )
