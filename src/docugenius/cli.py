#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocuGenius CLI - Document to Markdown Converter
Main CLI interface using Click
"""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from .config import Config, load_config, save_config
from .converter import Converter, ConversionResult
from .utils import get_file_size, format_file_size

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="docugenius")
def cli():
    """DocuGenius CLI - Convert documents to Markdown format."""
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output directory")
@click.option("--extract-images", is_flag=True, help="Extract images from document")
@click.option("--split-threshold", type=int, default=500000, help="Document splitting threshold in characters")
@click.option("--overwrite", is_flag=True, help="Overwrite existing files")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def convert(
    file: str,
    output: Optional[str],
    extract_images: bool,
    split_threshold: int,
    overwrite: bool,
    verbose: bool,
):
    """Convert a single document to Markdown."""
    file_path = Path(file).resolve()

    # Load configuration
    config = load_config()

    # Override with command-line options
    if output:
        # Convert output path to absolute path
        output_path = Path(output).resolve()
        config.output_dir = str(output_path)
    if extract_images:
        config.extract_images = True
    if split_threshold:
        config.split_threshold = split_threshold

    # Check if file is supported
    if file_path.suffix.lower() not in config.supported_extensions:
        console.print(f"[red]Error: Unsupported file type: {file_path.suffix}[/red]")
        console.print(f"[yellow]Supported formats: {', '.join(config.supported_extensions)}[/yellow]")
        sys.exit(1)

    # Show file info
    file_size = get_file_size(file_path)
    console.print(f"[cyan]📄 Converting:[/cyan] {file_path.name}")
    console.print(f"[dim]Size: {format_file_size(file_size)}[/dim]")

    # Create converter
    converter = Converter(config)

    # Convert file
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Converting...", total=None)

        result: ConversionResult = converter.convert_file(
            file_path,
            extract_images=config.extract_images,
            split_threshold=config.split_threshold,
            overwrite=overwrite,
            verbose=verbose,
        )

    # Show result
    if result.success:
        console.print(f"[green]✅ Converted to:[/green] {result.output_path}")
        if result.images_extracted:
            console.print(f"[blue]🖼️ Extracted {result.images_extracted} images to:[/blue] {result.images_dir}")
    else:
        console.print(f"[red]❌ Conversion failed:[/red] {result.error}")
        sys.exit(1)


@cli.command()
@click.argument("folder", type=click.Path(exists=True, file_okay=False))
@click.option("-o", "--output", type=click.Path(), help="Output directory")
@click.option("--extract-images", is_flag=True, help="Extract images from documents")
@click.option("--recursive", is_flag=True, help="Recursively process subdirectories")
@click.option("--split-threshold", type=int, default=500000, help="Document splitting threshold in characters")
@click.option("--overwrite", is_flag=True, help="Overwrite existing files")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def convert_folder(
    folder: str,
    output: Optional[str],
    extract_images: bool,
    recursive: bool,
    split_threshold: int,
    overwrite: bool,
    verbose: bool,
):
    """Convert all supported documents in a folder."""
    folder_path = Path(folder).resolve()

    # Load configuration
    config = load_config()

    # Override with command-line options
    if output:
        # Convert output path to absolute path
        output_path = Path(output).resolve()
        config.output_dir = str(output_path)
    if extract_images:
        config.extract_images = True
    if split_threshold:
        config.split_threshold = split_threshold

    # Find all files
    files = []
    if recursive:
        files = [
            f for ext in config.supported_extensions
            for f in folder_path.rglob(f"*{ext}")
        ]
    else:
        files = [
            f for ext in config.supported_extensions
            for f in folder_path.glob(f"*{ext}")
        ]

    if not files:
        console.print(f"[yellow]No supported files found in {folder_path}[/yellow]")
        return

    console.print(f"[cyan]📁 Processing {len(files)} files in {folder_path}...[/cyan]")

    # Create converter
    converter = Converter(config)

    # Convert files
    success_count = 0
    failure_count = 0

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Converting...", total=len(files))

        for file_path in files:
            progress.update(task, description=f"Converting {file_path.name}...")

            result: ConversionResult = converter.convert_file(
                file_path,
                extract_images=config.extract_images,
                split_threshold=config.split_threshold,
                overwrite=overwrite,
                verbose=verbose,
            )

            if result.success:
                success_count += 1
            else:
                failure_count += 1
                console.print(f"[red]  ✗ {file_path.name}: {result.error}[/red]")

            progress.update(task, advance=1)

    # Show summary
    console.print()
    if failure_count == 0:
        console.print(f"[green]✅ Successfully converted {success_count} files[/green]")
    else:
        console.print(f"[yellow]⚠️  Converted {success_count} files, {failure_count} failed[/yellow]")


@cli.command()
@click.option("--auto-convert", is_flag=True, help="Enable auto-convert for new files")
@click.option("--output-dir", type=str, help="Output directory name")
@click.option("--extract-images", is_flag=True, help="Enable image extraction")
@click.option("--no-extract-images", is_flag=True, help="Disable image extraction")
def init(auto_convert: bool, output_dir: Optional[str], extract_images: bool, no_extract_images: bool):
    """Initialize project configuration."""
    # Check if config already exists
    config_path = Path.cwd() / ".docugenius.json"
    if config_path.exists():
        if not click.confirm(f"Configuration file already exists at {config_path}. Overwrite?"):
            console.print("[yellow]Aborted.[/yellow]")
            return

    # Create new config
    config = Config()
    if auto_convert:
        config.auto_convert = True
    if output_dir:
        config.output_dir = output_dir
    if extract_images:
        config.extract_images = True
    if no_extract_images:
        config.extract_images = False

    # Save config
    save_config(config, cwd=Path.cwd())
    
    console.print(f"[green]✅ Configuration saved to {config_path}[/green]")
    console.print(f"[dim]You can edit this file to customize DocuGenius behavior.[/dim]")


@cli.command()
def status():
    """Show CLI status and configuration."""
    console.print("[cyan]DocuGenius CLI Status[/cyan]")
    console.print()

    # Show version
    console.print(f"[dim]Version:[/dim] 1.0.0")
    console.print(f"[dim]Python:[/dim] {sys.version}")
    console.print()

    # Show configuration
    config = load_config()
    console.print("[cyan]Configuration:[/cyan]")
    console.print(f"[dim]Output Directory:[/dim] {config.output_dir}")
    console.print(f"[dim]Extract Images:[/dim] {config.extract_images}")
    console.print(f"[dim]Split Threshold:[/dim] {format_file_size(config.split_threshold)}")
    console.print(f"[dim]Supported Extensions:[/dim] {', '.join(config.supported_extensions)}")
    console.print()

    # Show config file location
    config_path = Path.cwd() / ".docugenius.json"
    if config_path.exists():
        console.print(f"[dim]Config File:[/dim] {config_path}")
    else:
        console.print("[yellow]No configuration file found in current directory[/yellow]")
        console.print("[dim]Run 'docugenius init' to create one[/dim]")


def main():
    """Main entry point for the CLI."""
    cli()
