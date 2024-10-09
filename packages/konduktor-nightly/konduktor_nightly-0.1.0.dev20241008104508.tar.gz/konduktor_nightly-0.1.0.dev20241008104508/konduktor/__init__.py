"""The Konduktor package."""

import os
import subprocess

# Replaced with the current commit when building the wheels.
_KONDUKTOR_COMMIT_SHA = "e3e7bda3db7d0733be4109854a1a19e2a0eb78b8"


def _get_git_commit():
    if "KONDUKTOR_COMMIT_SHA" not in _KONDUKTOR_COMMIT_SHA:
        # This is a release build, so we don't need to get the commit hash from
        # git, as it's already been set.
        return _KONDUKTOR_COMMIT_SHA

    # This is a development build (pip install -e .), so we need to get the
    # commit hash from git.
    try:
        cwd = os.path.dirname(__file__)
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        changes = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if changes:
            commit_hash += "-dirty"
        return commit_hash
    except Exception:  # pylint: disable=broad-except
        return _KONDUKTOR_COMMIT_SHA


__commit__ = _get_git_commit()
__version__ = "1.0.0-dev0"
__root_dir__ = os.path.dirname(os.path.abspath(__file__))
