# DocuGenius CLI 快速开始指南

## 安装

```bash
uv tool install docugenius-cli --force --from git+https://github.com/bruc3van/docugenius.git
```

## 基本使用

### 1. 转换单个文件

```bash
docugenius convert document.docx
```

### 2. 转换并提取图片

```bash
docugenius convert document.docx --extract-images
```

### 3. 指定输出目录

```bash
docugenius convert document.docx --output ./output
```

### 4. 批量转换文件夹

```bash
docugenius convert-folder ./documents
```

### 5. 递归转换子目录

```bash
docugenius convert-folder ./documents --recursive
```

### 6. 初始化项目配置

```bash
docugenius init --output-dir kb --extract-images
```

这会创建 `.docugenius.json` 配置文件：

```json
{
  "version": "1.0",
  "autoConvert": true,
  "outputDir": "kb",
  "extractImages": true,
  "splitThreshold": 500000,
  "supportedExtensions": [".docx", ".xlsx", ".pptx", ".pdf"]
}
```

### 7. 查看状态

```bash
docugenius status
```

## 支持的格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Word | `.docx` | 保留文本层级 |
| Excel | `.xlsx` | 转换为 Markdown 表格 |
| PowerPoint | `.pptx` | 逐页提取文本和图片 |
| PDF | `.pdf` | 高质量文字提取 |

## 输出结构

```
project/
├── documents/
│   ├── report.docx
│   └── data.xlsx
├── kb/                      # 输出目录
│   ├── report.md
│   ├── data.md
│   └── images/
│       ├── report/
│       │   ├── image1.png
│       │   └── image2.png
│       └── data/
└── .docugenius.json         # 配置文件
```

## 高级选项

### 文档分割

大文档（超过 500KB）会自动分割为多个文件：

```bash
docugenius convert large.docx --split-threshold 1000000
```

输出：
- `large_part1.md`
- `large_part2.md`
- `large_index.md` (目录)

### 覆盖现有文件

```bash
docugenius convert document.docx --overwrite
```

### 详细输出

```bash
docugenius convert document.docx --verbose
```

## AI 调用示例

### Python

```python
import subprocess

result = subprocess.run(
    ["docugenius", "convert", "document.docx", "--extract-images"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

### Shell

```bash
# 转换并读取输出
docugenius convert document.docx --output ./output
cat ./output/document.md
```

## 故障排除

### 依赖缺失

```bash
uv tool install docugenius-cli --force --from git+https://github.com/bruc3van/docugenius.git
```

### 图片提取失败

某些文档可能包含损坏的图片，DocuGenius 会跳过这些图片并继续转换。

### 大文档分割

文档超过分割阈值（默认 500KB）时会自动分割，可通过 `--split-threshold` 调整。

