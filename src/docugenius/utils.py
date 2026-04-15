#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for DocuGenius CLI
"""

from pathlib import Path


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes
    """
    return file_path.stat().st_size


def format_file_size(size: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def split_by_headers(content: str) -> list[str]:
    """
    Split markdown content by headers.

    Args:
        content: Markdown content

    Returns:
        List of content sections
    """
    import re

    # Split by ## or ### headers
    sections = re.split(r"\n(?=#{2,3}\s)", content)
    return [s.strip() for s in sections if s.strip()]


def create_index_file(filename: str, part_count: int, base_name: str) -> str:
    """
    Create index file content for split documents.

    Args:
        filename: Original filename
        part_count: Number of parts
        base_name: Base name for part files

    Returns:
        Index file content as string
    """
    content = f"# {filename} - Index\n\n"
    content += "This document has been split into multiple parts:\n\n"
    for i in range(1, part_count + 1):
        content += f"- [Part {i}]({base_name}_part{i}.md)\n"
    return content
