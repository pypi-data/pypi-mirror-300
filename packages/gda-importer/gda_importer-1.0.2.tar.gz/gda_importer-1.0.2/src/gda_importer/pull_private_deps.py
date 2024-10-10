#!/bin/env python3

r"""Pull private deps by whatever means necessary.

This file is based on the GDA-Cookiecutter, version 2.5.0.
In most cases, it should not need to be edited by hand. In the unlikely scenario that
you need to change it in non-trivial ways, remove it from `.gda-cookiecutter_pathspec_tools`
so that future applications of GDA-Cookiecutter are easier to merge.
See https://gitlab.geomdata.com/geomdata/gda-cookiecutter/-/blob/master/README.md
for instructions on how to update to a newer version of the GDA-Cookiecutter.

This standalone script is Geometric Data Analytics (c) 2024, available under AGPLv3,
regardless of the other contents of the package it was included with.
"""

import argparse
import json
import logging
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

import toml
from packaging.requirements import SpecifierSet
from packaging.version import InvalidVersion, Version

# This throws annoying warnings. Suppress them
logging.captureWarnings(True)
log = logging.getLogger()
log.setLevel(logging.WARNING)

description = (
    "Pull private python (pip) requirements using fallback GitLab authententicaton."
)

epilog = "See DEPENDENCIES.md and the example in private-deps.toml for more detail."


def get_token(token_var):
    """Get the token from the environment or error."""
    if token_var in os.environ and len(os.environ[token_var]) > 0:
        return os.environ[token_var]
    log.warning(f"Environmental variable {token_var} is missing.")
    return None


def clone(
    name: str,
    gitlab_host: str,
    gitlab_path: str,
    gitlab_spec: str | None,
    token_var: str = "CI_JOB_TOKEN",
    **kwargs,
):
    """Try to clone this project, but not pip-install it."""
    cmd = ["git", "clone"]
    if gitlab_spec:
        cmd.extend(["-b", gitlab_spec])
    else:
        log.warning("No gitlab_spec provided. The default branch will be used.")
    if "SSH_AUTH_SOCK" in os.environ and os.environ["SSH_AUTH_SOCK"]:
        log.warning("Trying to use SSH credentials.")
        end_cmd = [f"git@{gitlab_host}:{gitlab_path}.git", name]
    else:
        token = get_token(token_var)
        end_cmd = [
            f"https://gitlab:{token}@{gitlab_host}/{gitlab_path}.git",
            name,
        ]
    return cmd + end_cmd


def installer(
    name: str,
    extras: list,
    gitlab_host: str,
    gitlab_path: str,
    gitlab_spec: str | None,
    version_set: str,
    token_var: str = "CI_JOB_TOKEN",
    always_pull: bool = False,
    no_deps: bool = False,
    dry_run: bool = False,
    force_src: bool = False,
    local: bool = False,
):
    """Try to install this package, either in CI, or locally, or via SSH."""
    # We hit Kaniko only in the prebuild CI stage for caching our toolchain.
    # Kaniko cannot grab the env vars. Need to load from JSON.
    kaniko_file = Path("/kaniko/.docker/config.json")
    we_are_in_kaniko = False
    if kaniko_file.exists():
        we_are_in_kaniko = True
        log.warning("We are in a Kaniko build. Reloading env vars from JSON.")
        kaniko_config = json.load(kaniko_file.open())
        for varname in [
            "CI",
            "CI_JOB_NAME",
            "CI_JOB_STAGE",
            "CI_JOB_TOKEN",
            "CI_PROJECT_NAME",
            token_var,
        ]:
            if varname in kaniko_config:
                os.environ[varname] = kaniko_config[varname]
                log.warning(f"Saving variable {varname} to env from kaniko")

    if "CI" in os.environ and os.environ["CI"] == "true":
        log.warning(
            f"We are in CI at stage {os.environ['CI_JOB_STAGE']} job {os.environ['CI_JOB_NAME']}"  # noqa: E501
        )
        # We hit Kaniko only in the prebuild CI stage for caching our toolchain.
        # So, this should be used ONLY IF always_pull is False
        if we_are_in_kaniko and always_pull:
            # Abort early so we don't cache in kaniko build
            log.warning(f"Skipping {name} due to 'always_pull' option {always_pull}")
            return None
        token_var = "CI_JOB_TOKEN"

    token = get_token(token_var)
    extras_str = ""
    if extras is not None and len(extras) > 0:
        extras_str = "[" + ",".join(extras) + "]"

    # Overall control logic, trying to be as efficient as possible.
    # If use_local is True, we look for a local clone.
    # If force_src is False, we can pull the wheel!
    # Otherwise, we try to pull the source.
    path = Path(os.path.pardir, name)
    git = Path(path, ".git")
    if local and git.exists() and git.is_dir():
        log.warning(
            f"Using local clone at {path}. gitlab_spec and version_set ignored!"
        )
        path = Path(os.path.pardir, name)
        end_cmd = ["-e", f"{path}"]
    elif token and not force_src:
        log.info("Pulling from private registry index.")
        url_path = quote(gitlab_path, safe="")  # URLEncode the group and project name.
        end_cmd = [
            f"{name}{extras_str}{SpecifierSet(version_set)}",
            "--index-url",
            f"https://gitlab-ci-token:{token}@{gitlab_host}/api/v4/projects/{url_path}/packages/pypi/simple",
        ]
    elif token and force_src:
        log.warning("Reverting to direct HTTP install.")
        if not gitlab_spec:
            gitlab_spec_str = ""
            log.warning("No gitlab_spec provided. The default branch will be used.")
        else:
            gitlab_spec_str = "@" + gitlab_spec
        end_cmd = [
            f"{name}{extras_str}@git+https://gitlab-ci-token:{token}@{gitlab_host}/{gitlab_path}.git{gitlab_spec_str}"
        ]
    else:
        log.warning("Pulling via SSH.  Hopefully your credentials work.")
        if not gitlab_spec:
            gitlab_spec_str = ""
            log.warning("No gitlab_spec provided. The default branch will be used.")
        else:
            gitlab_spec_str = "@" + gitlab_spec
        end_cmd = [
            f"{name}{extras_str}@git+ssh://git@{gitlab_host}/{gitlab_path}.git{gitlab_spec_str}"
        ]

    cmd = ["pip", "install", "-v"]
    if always_pull:
        cmd.append("-U")  # force newest version, even if there was a cache
    if no_deps:
        cmd.append("--no-deps")
    return cmd + end_cmd


# regex from PEP-345
# See https://packaging.python.org/en/latest/specifications/dependency-specifiers/#names
name_extras_re = re.compile(
    r"^(?P<name>[A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])($|\[(?P<extras>.*)\]$)",
    flags=re.IGNORECASE,
)


# This stanza also appears in gda_share_out/models.py
def spec_meets_version(force_src: bool, gitlab_spec: str | None, version_set: str):
    """Check whether a force_src, gitlab_spec, and version_set are compatible. Raises exceptions."""
    pip_set = SpecifierSet(version_set)
    if force_src:
        if gitlab_spec is None or pip_set:
            raise ValueError(
                "Option 'force_src=true' prohibits a version_set and requires a gitlab_spec."
            )
        else:
            return True
    else:
        if gitlab_spec is None:
            return True
        else:
            try:
                # This allows the leading 'v'
                # https://peps.python.org/pep-0440/#preceding-v-character
                version = Version(gitlab_spec)
                if version in pip_set:
                    logging.warning(
                        f"gitlab_spec {gitlab_spec} is compatible with version_set {pip_set}, "
                        "but it is unwise to use both. version_set takes precedence."
                    )
                    return True
                else:
                    raise ValueError(
                        "Version implied by gitlab_spec "
                        "is not included in the version_set."
                    )
            except (InvalidVersion, TypeError):
                raise ValueError(
                    f"gitlab_spec '{gitlab_spec}' does not represent a release number. "
                    "The version_set cannot be checked. "
                    "This requires 'force_src=true'. "
                    "Be wary of dependency drift on branches. "
                )
    raise ValueError("Unknown Case")  # should never reach.


def main():
    """Run CLI."""
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--toml",
        type=str,
        default="private-deps.toml",
        help="Path to private deps TOML file.",
    )
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        help="Use local clone at ../package-name if it exists.",
    )
    parser.add_argument(
        "-c",
        "--clone",
        action="store_true",
        help="Try to clone the source (instead of pip-installing), allowing --local ",
    )
    parser.add_argument(
        "-n",
        "--dry_run",
        action="store_true",
        help="Show the command, but do not run it.",
    )

    args = parser.parse_args()
    toml_dict = toml.load(args.toml)

    for name_and_extras, info in toml_dict.items():
        # Ideally, this would be pydantic, but this script must stand alone.
        assert "gitlab_host" in info, epilog
        assert "gitlab_path" in info, epilog
        if "force_src" not in info:
            info["force_src"] = False
        if "gitlab_spec" not in info:
            info["gitlab_spec"] = None
        if "version_set" not in info:
            info["version_set"] = ""

        spec_meets_version(info["force_src"], info["gitlab_spec"], info["version_set"])
        log.info(f"Found private dependency {name_and_extras} in {args.toml}")
        re_match = name_extras_re.match(name_and_extras)
        if re_match is None:
            raise ValueError(
                f"The header '{name_and_extras}' is not a valid as 'package-name[extras]'."
            )
        name = re_match.group("name")
        extras = re_match.group("extras")
        if extras is not None:
            extras = extras.split(",")
        log.info(f"Processing '{name}' with extras {extras} in {args.toml}")
        if args.clone:
            total_cmd = clone(name, **info)
        else:
            total_cmd = installer(name, extras, **info, local=args.local)

        if total_cmd:
            if args.dry_run:
                log.info("Here is your command. You might need quotes.")
                print(" ".join(total_cmd))
            else:
                subprocess.run(total_cmd, check=True)


if __name__ == "__main__":
    main()
