# get-bibtex

A Python tool for fetching citations from multiple sources.

[![PyPI version](https://badge.fury.io/py/get-bibtex.svg)](https://badge.fury.io/py/get-bibtex)
[![Python Version](https://img.shields.io/pypi/pyversions/get-bibtex.svg)](https://pypi.org/project/get-bibtex/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[中文文档](README_CN.md)

## Features

- Multiple data sources (CrossRef, DBLP, Google Scholar)
- Smart workflow and fallback mechanism
- Batch processing
- Detailed error handling and logging

## Quick Start

### Installation

```bash
pip install get-bibtex
```

### Basic Usage

```python
from apiModels import CrossRefBibTeX

# Using CrossRef
fetcher = CrossRefBibTeX(email="your.email@example.com")
bibtex = fetcher.get_bibtex("10.3390/s22197244")  # FedMSA paper
print(bibtex)
```

### Using Workflow

```python
from apiModels import WorkflowBuilder, CrossRefBibTeX, DBLPBibTeX

# Create workflow
workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# Batch processing
queries = [
    "ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks",
    "CBAM: Convolutional Block Attention Module"
]
results = workflow.get_multiple_bibtex(queries)
```

## Using Google Scholar

### Getting SerpAPI Key

1. Visit [SerpAPI](https://serpapi.com/) and sign up
2. Get API key from Dashboard
3. Initialize Google Scholar fetcher with API key

```python
from apiModels import GoogleScholarBibTeX

fetcher = GoogleScholarBibTeX(api_key="your-serpapi-key")
bibtex = fetcher.get_bibtex("Attention Is All You Need")
print(bibtex)
```

### Notes

- Free plan limited to 100 searches per month
- Use environment variables for API key
- Prefer CrossRef and DBLP when possible

## Examples

### Fetching Attention Mechanism Papers

```python
from apiModels import CrossRefBibTeX

fetcher = CrossRefBibTeX(email="your.email@example.com")

# Get ECA-Net paper citation
bibtex = fetcher.get_bibtex("10.1109/cvpr42600.2020.01155")
print(bibtex)
```

### File Processing

```python
from apiModels import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_fetcher(CrossRefBibTeX(email="your.email@example.com"))
workflow.add_fetcher(DBLPBibTeX())

# Read queries from file and save results
workflow.process_file("papers.txt", "references.bib")
```

## Documentation

For detailed documentation, see [blog_cn.md](blog_cn.md)

## Contributing

Pull requests and issues are welcome!

## License

MIT
