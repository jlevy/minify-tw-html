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
from pathlib import Path

from .main import minify_tw_html


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("src_html", type=Path, help="Input HTML file.")
    parser.add_argument("dest_html", type=Path, help="Output HTML file.")
    parser.add_argument(
        "--no-minify",
        action="store_true",
        help="Skip HTML minification (only compile Tailwind if present).",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging.")

    args = parser.parse_args()

    # Set up logging with clean output for CLI usage
    if args.verbose:
        # Verbose mode: include level names for debugging
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    else:
        # Default mode: clean output without level prefixes
        logging.basicConfig(level=logging.WARNING, format="%(message)s")

    minify_tw_html(args.src_html, args.dest_html, minify_html=not args.no_minify)


if __name__ == "__main__":
    main()
