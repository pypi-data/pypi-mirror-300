"""SCM Commit base class."""

import logging

log = logging.getLogger(__name__)


class Commit:
    """
    Keep SCM commit info.

    Info includea scm type, path, tag, commit count and hash.
    """

    Name = "scm"

    @staticmethod
    def supported(path: str) -> bool:
        log.debug("unsupported %s", path)
        return False

    def __init__(self) -> None:
        self.info = {
            "type": self.Name,
            "tag": "0.1.0",
            "count": "0",
            "hash": "deadbeaf",
        }
