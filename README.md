# DocuGenius CLI

> Convert Word, Excel, PowerPoint, and PDF documents to Markdown format

[![PyPI version](https://badge.fury.io/py/docugenius-cli.svg)](https://badge.fury.io/py/docugenius-cli)
[![Python version](https://img.shields.io/pypi/pyversions/docugenius-cli.svg)](https://pypi.org/project/docugenius-cli/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

DocuGenius CLI is a command-line tool that converts various document formats to structured Markdown, making it easy for AI tools to understand your business documents.

## Features

- 📄 **Multiple Format Support**: Word (`.docx`), Excel (`.xlsx`), PowerPoint (`.pptx`), PDF (`.pdf`)
- 🖼️ **Image Extraction**: Automatically extract and organize images from documents
- 📁 **Batch Conversion**: Convert entire folders with a single command
- ⚡ **Local Processing**: All conversions happen locally - no data uploaded to cloud
- 🎨 **Rich Output**: Beautiful progress bars and colored terminal output
- ⚙️ **Configurable**: Support for project-level configuration files

## Installation

```bash
uv tool install docugenius-cli --force --from git+https://github.com/bruc3van/docugenius.git
```

## Quick Start

### Convert a single file

```bash
docugenius convert document.docx
```

### Convert with image extraction

```bash
docugenius convert document.docx --extract-images
```

### Convert to custom output directory

```bash
docugenius convert document.docx --output ./output
```

### Batch convert a folder

```bash
docugenius convert-folder ./docs
```

### Initialize project configuration

```bash
docugenius init
```

This creates a `.docugenius.json` file in your project root:

```json
{
  "version": "1.0",
  "autoConvert": true,
  "outputDir": "DocuGenius",
  "extractImages": true,
  "splitThreshold": 500000,
  "supportedExtensions": [".docx", ".xlsx", ".pptx", ".pdf"]
}
```

## Commands

### `convert`

Convert a single document to Markdown.

```bash
docugenius convert [OPTIONS] FILE
```

**Options:**
- `-o, --output PATH`: Output directory (default: DocuGenius)
- `--extract-images`: Extract images from document
- `--split-threshold INTEGER`: Document splitting threshold in characters (default: 500000)
- `--overwrite`: Overwrite existing files
- `-v, --verbose`: Enable verbose output

### `convert-folder`

Convert all supported documents in a folder.

```bash
docugenius convert-folder [OPTIONS] FOLDER
```

**Options:**
- `-o, --output PATH`: Output directory (default: DocuGenius)
- `--extract-images`: Extract images from documents
- `--recursive`: Recursively process subdirectories
- `--split-threshold INTEGER`: Document splitting threshold in characters
- `--overwrite`: Overwrite existing files
- `-v, --verbose`: Enable verbose output

### `init`

Initialize project configuration.

```bash
docugenius init [OPTIONS]
```

**Options:**
- `--auto-convert`: Enable auto-convert for new files
- `--output-dir TEXT`: Output directory name
- `--extract-images`: Enable image extraction
- `--no-extract-images`: Disable image extraction

### `status`

Show CLI status and configuration.

```bash
docugenius status
```

## Configuration

DocuGenius CLI looks for configuration in the following order:

1. Command-line arguments
2. `.docugenius.json` in current directory
3. Default values

### Configuration File

Create a `.docugenius.json` file in your project root:

```json
{
  "version": "1.0",
  "autoConvert": true,
  "outputDir": "DocuGenius",
  "extractImages": true,
  "splitThreshold": 500000,
  "supportedExtensions": [".docx", ".xlsx", ".pptx", ".pdf"]
}
```

## Examples

### Convert a Word document with images

```bash
docugenius convert report.docx --extract-images --output ./output
```

Output:
```
📄 Converting report.docx...
✅ Converted to output/report.md
🖼️ Extracted 5 images to output/images/report/
```

### Batch convert all documents

```bash
docugenius convert-folder ./documents --recursive --extract-images
```

Output:
```
📁 Processing 12 files in ./documents...
████████████████████████████████████████ 12/12 100%
✅ Successfully converted 12 files
```

### Initialize a new project

```bash
docugenius init --auto-convert --output-dir kb --extract-images
```

## Output Structure

```
project/
├── documents/
│   ├── report.docx
│   └── data.xlsx
├── DocuGenius/              # Output directory
│   ├── report.md
│   ├── data.md
│   └── images/
│       ├── report/
│       │   ├── image1.png
│       │   └── image2.png
│       └── data/
└── .docugenius.json         # Configuration file
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Word | `.docx` | Preserves text hierarchy |
| Excel | `.xlsx` | Converts to Markdown tables |
| PowerPoint | `.pptx` | Extracts text and images per slide |
| PDF | `.pdf` | High-quality text extraction |

## Development

### Install from source

```bash
git clone https://github.com/bruc3van/docugenius.git
cd docugenius/docugenius-cli
uv sync
```

### Run tests

```bash
pytest
```

### Format code

```bash
black src/
```

## Troubleshooting

### Missing dependencies

If you see import errors, try reinstalling:

```bash
uv tool install docugenius-cli --force --from git+https://github.com/bruc3van/docugenius.git
```

### Image extraction fails

Some documents may have corrupted images. DocuGenius will skip corrupted images and continue conversion.

### Large document splitting

Documents larger than the split threshold (default: 500KB) are automatically split into multiple files:
- `document_part1.md`
- `document_part2.md`
- `document_index.md` (table of contents)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- X: [@bruc3van](https://x.com/bruc3van)
- GitHub: [@bruc3van](https://github.com/bruc3van)

## Related Projects

- [DocuGenius VSCode Extension](https://github.com/bruc3van/docugenius) - The VSCode extension version
