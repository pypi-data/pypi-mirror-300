"""Git Commit base class."""

import logging
import subprocess as sp

from .scm_common import Commit

log = logging.getLogger(__name__)


class GitCommit(Commit):
    """
    Keep GIT commit info.

    Info includea scm type, path, tag, commit count and hash.
    """

    Name = "git"

    @staticmethod
    def supported(path: str) -> bool:
        cmd = ["git", "-C", path, "rev-parse", "--git-dir"]
        p = sp.run(cmd, check=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        return p.returncode == 0

    def __init__(self, adir: str, aref: str):
        super().__init__()
        self.info["path"] = adir
        self.info["ref"] = aref

        def my_run(cmd: list[str]):
            log.debug("cmd %s", cmd)
            return sp.run(
                cmd, check=False, text=True, stdout=sp.PIPE, stderr=sp.DEVNULL
            )

        cmd = ["git", "-C", adir, "describe", "--abbrev=0", aref]
        p = my_run(cmd)
        txt = p.stdout.strip()
        if p.returncode:
            crange = aref
        else:
            self.info["tag"] = txt
            crange = f"{txt}..{aref}"

        cmd = ["git", "-C", adir, "rev-list", crange, "--count"]
        p = my_run(cmd)
        txt = p.stdout.strip()
        self.info["count"] = txt

        cmd = ["git", "-C", adir, "rev-parse", "--short", aref]
        p = my_run(cmd)
        txt = p.stdout.strip()
        self.info["hash"] = txt
