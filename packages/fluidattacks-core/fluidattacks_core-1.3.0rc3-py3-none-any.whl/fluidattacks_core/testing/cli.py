from .aws.plugins import (
    MotoPlugin,
)
from .plugins import (
    CustomFixturesPlugin,
)
import argparse
import coverage
import os
import pathlib
import pytest as _pytest
import sys as _sys
from typing import (
    NamedTuple,
)


class Args(NamedTuple):
    target: pathlib.Path
    scope: str | None
    include_coverage: bool


def get_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="fluidattacks_core.testing",
        description=(
            "🏹 Python package for unit and integration testing through "
            "Fluid Attacks projects 🏹"
        ),
    )

    parser.add_argument(
        "--target",
        metavar="TARGET",
        type=pathlib.Path,
        default=os.getcwd(),
        help="Directory to start the tests. Default is current directory.",
    )

    parser.add_argument(
        "--scope",
        metavar="SCOPE",
        type=str,
        default=None,
        help="Type and module to test.",
    )

    parser.add_argument(
        "--include-coverage",
        type=bool,
        default=False,
        help="Generate a coverage report in stdout. Default is False.",
    )
    args = parser.parse_args()

    return Args(
        target=args.target,
        scope=args.scope,
        include_coverage=args.include_coverage,
    )


def _run(args: Args, pytest_args: list[str]) -> int:
    if args.include_coverage:
        cov = coverage.Coverage()
        cov.set_option("run:source", [f"{args.target}/{args.scope}"])
        cov.start()

    result = _pytest.main(
        [str(args.target), *pytest_args],
        plugins=[
            CustomFixturesPlugin(),
            MotoPlugin(),
        ],
    )

    if args.include_coverage:
        cov.stop()
        cov.report(
            include=[f"{args.target}/{args.scope}/*"],
            output_format="text",
            skip_covered=True,
            skip_empty=True,
            sort="cover",
        )

    return result


def execute() -> None:
    args = get_args()

    _scope_args = ["-m", f"{args.scope}"] if args.scope else []
    pytest_args = [
        "--disable-warnings",
        "--showlocals",
        "--strict-markers",
        "--verbose",
        *_scope_args,
    ]
    _sys.exit(_run(args, pytest_args))
