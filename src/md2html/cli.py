#!/usr/bin/env python3
"""
Command Line Interface for md2html

Provides a user-friendly CLI for converting Markdown files to HTML
with support for themes, table of contents, and batch processing.

Usage:
    md2html input.md                    # Convert to input.html
    md2html input.md -o output.html     # Specify output file
    md2html input.md --theme dark       # Use dark theme
    md2html input.md --no-toc           # Disable table of contents
    md2html *.md -d output/             # Batch convert to directory

Author: Carlos Crespo
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__, __author__
from .parser import MarkdownParser
from .converter import HTMLConverter
from .styles import Theme


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="md2html",
        description="Convert Markdown files to beautifully styled HTML",
        epilog=f"Created by {__author__} | Version {__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Positional arguments
    parser.add_argument(
        "input", nargs="+", type=str, help="Input Markdown file(s) to convert"
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (default: input filename with .html extension)",
    )
    output_group.add_argument(
        "-d",
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for batch conversions",
    )

    # Styling options
    style_group = parser.add_argument_group("Styling Options")
    style_group.add_argument(
        "-t",
        "--theme",
        type=str,
        choices=["light", "dark"],
        default="light",
        help="Color theme for the output (default: light)",
    )
    style_group.add_argument(
        "--no-styles", action="store_true", help="Exclude CSS styles from output"
    )
    style_group.add_argument(
        "--minimal-styles",
        action="store_true",
        help="Use minimal CSS instead of full styles",
    )

    # Content options
    content_group = parser.add_argument_group("Content Options")
    content_group.add_argument(
        "--no-toc", action="store_true", help="Disable table of contents generation"
    )
    content_group.add_argument(
        "--toc-title",
        type=str,
        default="Table of Contents",
        help="Custom title for table of contents",
    )
    content_group.add_argument(
        "--title",
        type=str,
        default=None,
        help="Document title (default: derived from filename or first h1)",
    )

    # Fragment mode
    parser.add_argument(
        "--fragment",
        action="store_true",
        help="Output HTML fragment without document wrapper",
    )

    # Utility options
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress output messages"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without creating files",
    )

    return parser


def get_output_path(
    input_path: Path, output: Optional[str], output_dir: Optional[str]
) -> Path:
    """
    Determine the output file path.

    Args:
        input_path: The input Markdown file path.
        output: Explicit output path from arguments.
        output_dir: Output directory from arguments.

    Returns:
        Path object for the output file.
    """
    if output:
        return Path(output)

    output_filename = input_path.stem + ".html"

    if output_dir:
        return Path(output_dir) / output_filename

    return input_path.parent / output_filename


def extract_title(markdown_text: str, filepath: Path) -> str:
    """
    Extract a title from Markdown content or filename.

    Looks for the first h1 heading, falls back to filename.

    Args:
        markdown_text: The Markdown content.
        filepath: Path to the input file.

    Returns:
        A suitable title string.
    """
    # Look for first h1 heading
    for line in markdown_text.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()

    # Fall back to filename
    return filepath.stem.replace("-", " ").replace("_", " ").title()


def convert_file(
    input_path: Path, output_path: Path, args: argparse.Namespace, quiet: bool = False
) -> bool:
    """
    Convert a single Markdown file to HTML.

    Args:
        input_path: Path to input Markdown file.
        output_path: Path for output HTML file.
        args: Parsed command line arguments.
        quiet: Suppress progress messages.

    Returns:
        True if conversion successful, False otherwise.
    """
    try:
        # Read input file
        markdown_text = input_path.read_text(encoding="utf-8")

        # Determine title
        title = args.title or extract_title(markdown_text, input_path)

        # Select theme
        theme = Theme.DARK if args.theme == "dark" else Theme.LIGHT

        # Parse Markdown
        parser = MarkdownParser()
        tokens = parser.parse(markdown_text)
        headers = parser.get_headers()

        # Create converter
        converter = HTMLConverter(
            theme=theme,
            include_toc=not args.no_toc,
            toc_title=args.toc_title,
            include_styles=not args.no_styles,
        )

        # Convert to HTML
        if args.fragment:
            html = converter.convert_fragment(tokens)
        else:
            html = converter.convert(tokens, title=title, headers=headers)

        # Handle dry run
        if args.dry_run:
            if not quiet:
                print(f"Would convert: {input_path} -> {output_path}")
            return True

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output file
        output_path.write_text(html, encoding="utf-8")

        if not quiet:
            print(f"✓ Converted: {input_path} -> {output_path}")

        return True

    except FileNotFoundError:
        print(f"✗ Error: File not found: {input_path}", file=sys.stderr)
        return False
    except PermissionError:
        print(f"✗ Error: Permission denied: {output_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Error converting {input_path}: {e}", file=sys.stderr)
        return False


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        argv: Command line arguments (default: sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parser = create_argument_parser()
    args = parser.parse_args(argv)

    # Collect input files
    input_files: List[Path] = []
    for pattern in args.input:
        path = Path(pattern)
        if path.exists():
            input_files.append(path)
        else:
            # Try glob expansion
            expanded = list(Path(".").glob(pattern))
            if expanded:
                input_files.extend(expanded)
            else:
                print(f"Warning: No files match pattern: {pattern}", file=sys.stderr)

    if not input_files:
        print("Error: No input files found", file=sys.stderr)
        return 1

    # Validate single file output option
    if args.output and len(input_files) > 1:
        print(
            "Error: Cannot use -o/--output with multiple input files. "
            "Use -d/--output-dir instead.",
            file=sys.stderr,
        )
        return 1

    # Process files
    success_count = 0
    error_count = 0

    for input_path in input_files:
        output_path = get_output_path(input_path, args.output, args.output_dir)

        if convert_file(input_path, output_path, args, quiet=args.quiet):
            success_count += 1
        else:
            error_count += 1

    # Summary for batch operations
    if len(input_files) > 1 and not args.quiet:
        print(
            f"\nProcessed {len(input_files)} files: "
            f"{success_count} success, {error_count} errors"
        )

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
