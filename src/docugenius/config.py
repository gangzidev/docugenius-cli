#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for DocuGenius CLI
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


@dataclass
class Config:
    """Configuration for DocuGenius CLI."""

    version: str = "1.0"
    auto_convert: bool = True
    output_dir: str = "DocuGenius"
    extract_images: bool = True
    split_threshold: int = 500000
    supported_extensions: List[str] = None

    def __post_init__(self):
        if self.supported_extensions is None:
            self.supported_extensions = [".docx", ".xlsx", ".pptx", ".pdf"]


def load_config(cwd: Optional[Path] = None) -> Config:
    """
    Load configuration from .docugenius.json file.

    Args:
        cwd: Current working directory (defaults to Path.cwd())

    Returns:
        Config object with loaded values
    """
    if cwd is None:
        cwd = Path.cwd()

    config_path = cwd / ".docugenius.json"

    if not config_path.exists():
        return Config()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Config(**data)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Warning: Failed to load config file: {e}")
        return Config()


def save_config(config: Config, cwd: Optional[Path] = None) -> None:
    """
    Save configuration to .docugenius.json file.

    Args:
        config: Config object to save
        cwd: Current working directory (defaults to Path.cwd())
    """
    if cwd is None:
        cwd = Path.cwd()

    config_path = cwd / ".docugenius.json"

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(asdict(config), f, indent=2)
