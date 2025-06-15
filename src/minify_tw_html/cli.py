#!/usr/bin/env python
"""
CLI for HTML minification with Tailwind CSS v4 compilation.

This script can be used for general HTML minification (including inline CSS/JS) and/or
Tailwind CSS v4 compilation and inlining (replacing CDN script with compiled CSS).

Minification includes:
- HTML structure: whitespace removal, comment removal
- Inline CSS: all <style> tags and style attributes are minified
- Inline JavaScript: all <script> tags are minified (not external JS files)
"""

import argparse
import logging
from importlib.metadata import version
from pathlib import Path
from textwrap import dedent

from .main import minify_tw_html

APP_NAME = "minify-tw-html"

DESCRIPTION = """HTML minification with Tailwind CSS v4 compilation"""


def get_version_name() -> str:
    """Get formatted version string"""
    try:
        app_version = version(APP_NAME)
        return f"{APP_NAME} v{app_version}"
    except Exception:
        return "(unknown version)"


def build_parser() -> argparse.ArgumentParser:
    """Build the main argument parser"""
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent((__doc__ or "") + "\n\n" + get_version_name()),
    )

    parser.add_argument("--version", action="version", version=get_version_name())
    parser.add_argument("src_html", type=Path, help="Input HTML file.")
    parser.add_argument("dest_html", type=Path, help="Output HTML file.")
    parser.add_argument(
        "--no-minify",
        action="store_true",
        help="Skip HTML minification (only compile Tailwind if present).",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Enable Tailwind's preflight CSS reset (disabled by default to preserve custom styles).",
    )
    parser.add_argument(
        "--tailwind",
        action="store_true",
        help="Force Tailwind CSS compilation even if CDN script is not present.",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging.")

    return parser


def main():
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format="%(message)s")

    minify_tw_html(
        args.src_html,
        args.dest_html,
        minify_html=not args.no_minify,
        preflight=args.preflight,
        force_tailwind=args.tailwind,
    )


if __name__ == "__main__":
    main()
