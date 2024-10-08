from typing import Union
import requests
from ..result_with_err import ResultWithErr, OK, ERR
from .extension_details import VscodeExtensionDetails


def retrieve_vscode_ext_details(
    extension_id,
) -> ResultWithErr[VscodeExtensionDetails]:
    """
    Retrieves the details of a Visual Studio Code extension from the Visual Studio Marketplace API.

    This function makes a series of API requests to the Visual Studio Marketplace to fetch the details of a given extension, including its last updated date and short description. It uses pagination to fetch all the results, as the API has a limit on the number of results returned per request.

    Args:
        extension_id (str): The unique identifier of the Visual Studio Code extension.

    Yields:
        VscodeExtension: An object containing the extension's ID, last updated date, and short description.
    """
    max_page = 10000
    page_size = 100
    api_version = "7.2-preview.1"
    flags = 33411

    for page in range(1, max_page + 1):
        body = {
            "filters": [
                {
                    "criteria": [{"filterType": 7, "value": extension_id}],
                    "pageNumber": page,
                    "pageSize": page_size,
                    "sortBy": 0,
                    "sortOrder": 0,
                }
            ],
            "assetTypes": [],
            "flags": flags,
        }

        response = requests.post(
            "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery",
            headers={
                "Accept": f"application/json; charset=utf-8; api-version={api_version}",
                "Content-Type": "application/json",
            },
            json=body,
        )

        if response.ok:
            data = response.json()
            extensions = data["results"][0]["extensions"]
            if extensions:
                for ext in extensions:
                    ret = VscodeExtensionDetails.from_dict(ext)
                    return OK(ret)
    return ERR(Exception(f"Error fetching data for extension {extension_id}"))
