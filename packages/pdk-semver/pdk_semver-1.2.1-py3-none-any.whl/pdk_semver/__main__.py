"""
Pretty print project's versions in different styles.

EPILOG:
$ pdk-semver -s all --extra some.info
internal  3.2.2-rev.3.some.info.git.b674019
  public  3.2.2-rev.3.some.info
    base  3.2.2-some.info

$ pdk-semver
3.2.2-rev.3.git.b674019

$ pdk-semver --extra arch.aarch64
3.2.2-rev.3.arch.aarch64.git.b674019
"""

import logging
import sys

import pydevkit.log.config  # noqa: F401
from pydevkit.argparse import ArgumentParser

from . import __version__
from .scm import get_commit
from .ver import Version

log = logging.getLogger(__name__)


def get_cmd_vals(args: object) -> dict[str, str]:
    vals: dict[str, str] = {}
    for k, v in vars(args).items():
        pfx = k.split("_", 1)[0]
        if pfx in ["rinfo"]:
            vals[k] = v
    return vals


def get_args():
    p = ArgumentParser(help=__doc__, version=__version__, usage="short")
    p.add_argument(
        "-C", help="path to git repo", dest="path", metavar="path", default="."
    )
    p.add_argument(
        "-r", help="git revision ref", dest="ref", metavar="ref", default="HEAD"
    )
    styles = [*list(Version.Styles.keys()), "all"]
    p.add_argument(
        "-s",
        help="style, one of %(choices)s",
        dest="style",
        metavar="name",
        default="internal",
        choices=styles,
    )
    p.add_argument("--extra", help="extra info", metavar="txt", default="")

    return p.parse_known_args()


def main() -> None:
    args, unknown_args = get_args()
    if unknown_args:
        log.warning("Unknown arguments: %s", unknown_args)
        sys.exit(1)

    ver = Version(get_commit(args.path, args.ref))
    if args.style != "all":
        print(ver.fmt(args.style, args.extra))
        return

    for k in Version.Styles:
        print("%8s" % k, ver.fmt(k, args.extra))


if __name__ == "__main__":
    main()
