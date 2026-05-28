"""CLI entry point for aap-config-validate."""

from __future__ import annotations

import argparse
import sys
from typing import List

from aap_config_validate.loader import load_paths
from aap_config_validate.models import Issue, Severity
from aap_config_validate.reporter import report_json, report_text
from aap_config_validate.validators import merge_wildcard_vars, validate


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aap-config-validate",
        description="Validate AAP configuration files against infra.aap_configuration schemas.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="YAML files or directories to validate",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        dest="output_format",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Treat warnings as errors",
    )
    parser.add_argument(
        "--component",
        action="append",
        choices=["controller", "gateway", "hub", "eda"],
        dest="components",
        help="Limit validation to specific component(s); may be repeated",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        default=False,
        help="Disable coloured output",
    )
    parser.add_argument(
        "--show-info",
        action="store_true",
        default=False,
        help="Include INFO-level messages in output",
    )
    parser.add_argument(
        "--wildcard-vars",
        choices=["auto", "always", "never"],
        default="auto",
        help=(
            "Wildcard variable merging: 'auto' enables when "
            "dispatch_include_wildcard_vars is set in config (default), "
            "'always' forces merging, 'never' disables it"
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    config, load_errors = load_paths(args.paths)
    issues: List[Issue] = []

    for err in load_errors:
        issues.append(Issue(severity=Severity.ERROR, path="<loader>", message=err))

    if config:
        do_wildcard = args.wildcard_vars == "always" or (args.wildcard_vars == "auto" and config.get("dispatch_include_wildcard_vars", False))
        if do_wildcard:
            config, wildcard_issues = merge_wildcard_vars(config)
            issues.extend(wildcard_issues)
        issues.extend(validate(config, components=args.components))

    if not args.show_info:
        issues = [i for i in issues if i.severity is not Severity.INFO]

    if args.strict:
        for issue in issues:
            if issue.severity is Severity.WARNING:
                issue.severity = Severity.ERROR

    if args.output_format == "json":
        report_json(issues)
    else:
        report_text(issues, color=not args.no_color)

    has_errors = any(i.severity is Severity.ERROR for i in issues)
    sys.exit(1 if has_errors else 0)
