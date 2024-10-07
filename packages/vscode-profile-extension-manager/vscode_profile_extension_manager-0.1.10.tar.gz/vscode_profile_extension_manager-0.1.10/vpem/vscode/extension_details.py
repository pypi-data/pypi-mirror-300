from datetime import datetime
from typing import List
from prodict import Prodict


class _Publisher(Prodict):
    publisherId: str
    publisherName: str
    displayName: str
    flags: str
    domain: str | None
    isDomainVerified: bool


class VscodeExtensionDetails(Prodict):
    ext_id: str
    publisher: _Publisher
    extensionId: str
    extensionName: str
    displayName: str
    flags: str
    lastUpdated: str
    publishedDate: str
    releaseDate: str
    presentInConflictList: str
    shortDescription: str
    deploymentType: int
    profile: List[str]
    last_refreshed: str
    needs_refresh: bool

    @classmethod
    def from_dict(cls, data):
        ext_details = cls()
        ext_details.publisher = _Publisher.from_dict(data.get("publisher", {}))
        ext_details.extensionId = data.get("extensionId", "")
        ext_details.extensionName = data.get("extensionName", "")
        ext_details.displayName = data.get("displayName", "")
        ext_details.flags = data.get("flags", "")
        ext_details.lastUpdated = data.get("lastUpdated", "")
        ext_details.publishedDate = data.get("publishedDate", "")
        ext_details.releaseDate = data.get("releaseDate", "")
        ext_details.presentInConflictList = data.get("presentInConflictList", "")
        ext_details.shortDescription = data.get("shortDescription", "")
        ext_details.deploymentType = data.get("deploymentType", 0)
        ext_details.ext_id = (
            f"{ext_details.publisher.publisherName}.{ext_details.extensionName}"
        ).lower()
        ext_details.profile = data.get("profile", [])
        is_new = data.get("last_refreshed", "") == ""
        ext_details.last_refreshed = data.get(
            "last_refreshed", datetime.now().isoformat()
        )
        # needs_refresh is set to True if the last_refreshed date is more than 30 days ago
        ext_details.needs_refresh = (
            is_new
            or (
                datetime.now() - datetime.fromisoformat(ext_details.last_refreshed)
            ).days
            > 30
        )
        return ext_details
