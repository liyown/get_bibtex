# get-bibtex

一个用于从多个来源获取文献引用的 Python 工具包。

[![PyPI version](https://badge.fury.io/py/get-bibtex.svg)](https://badge.fury.io/py/get-bibtex)
[![Python Version](https://img.shields.io/pypi/pyversions/get-bibtex.svg)](https://pypi.org/project/get-bibtex/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md)

## 特点

- 支持多个数据源（CrossRef、DBLP、Google Scholar）
- 智能工作流和回退机制
- 批量处理功能
- 详细的错误处理和日志记录

## 快速开始

### 安装

```bash
pip install get-bibtex
```

### 基本使用

```python
from apiModels import CrossRefBibTeX

# 使用 CrossRef
fetcher = CrossRefBibTeX(email="your.email@example.com")
bibtex = fetcher.get_bibtex("10.3390/s22197244")  # FedMSA 论文
print(bibtex)
```

### 使用工作流

```python
from apiModels import WorkflowBuilder, CrossRefBibTeX, DBLPBibTeX

# 创建工作流
workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# 批量处理
queries = [
    "ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks",
    "CBAM: Convolutional Block Attention Module"
]
results = workflow.get_multiple_bibtex(queries)
```

## 使用 Google Scholar

### 获取 SerpAPI Key

1. 访问 [SerpAPI](https://serpapi.com/) 并注册账号
2. 在 Dashboard 获取 API key
3. 使用 API key 初始化 Google Scholar 获取器

```python
from apiModels import GoogleScholarBibTeX

fetcher = GoogleScholarBibTeX(api_key="your-serpapi-key")
bibtex = fetcher.get_bibtex("Attention Is All You Need")
print(bibtex)
```

### 注意事项

- 免费计划每月限制 100 次搜索
- 建议使用环境变量存储 API key
- 优先使用 CrossRef 和 DBLP

## 示例

### 获取注意力机制相关论文

```python
from apiModels import CrossRefBibTeX

fetcher = CrossRefBibTeX(email="your.email@example.com")

# 获取 ECA-Net 论文引用
bibtex = fetcher.get_bibtex("10.1109/cvpr42600.2020.01155")
print(bibtex)
```

### 文件批处理

```python
from apiModels import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# 从文件读取查询并保存结果
workflow.process_file("papers.txt", "references.bib")
```

## 文档

详细文档请参见 [blog_cn.md](blog_cn.md)

## 贡献

欢迎提交 Pull Request 或创建 Issue！

## 许可证

MIT

