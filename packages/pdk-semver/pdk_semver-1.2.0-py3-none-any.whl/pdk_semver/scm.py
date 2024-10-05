"""Git repo support."""

import logging
import sys

import pydevkit.log.config  # noqa: F401

from .scm_common import Commit
from .scm_git import GitCommit

log = logging.getLogger(__name__)


def get_commit(path: str, ref: str) -> Commit:
    """Return SCM commit."""

    for cls in [GitCommit]:
        if cls.supported(path):
            log.debug("%s repo found at '%s'", cls.Name, path)
            return cls(path, ref)

    log.warning("no version control found at '%s", path)
    sys.exit(1)
