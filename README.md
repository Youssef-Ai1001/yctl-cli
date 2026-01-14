# yctl

**Personal AI Engineer CLI Tool for Ubuntu**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful command-line tool that streamlines AI/ML development workflows. Built for AI engineers who value productivity, best practices, and beautiful terminal experiences.

## ✨ Features

- 🚀 **Project Initialization**: Create production-ready AI projects with one command
- 🔍 **Dataset Inspection**: Comprehensive dataset analysis with intelligent recommendations
- 🏥 **System Diagnostics**: Verify your AI development environment
- 💡 **AI Idea Analyzer**: Get expert guidance for your AI project ideas

## 📦 Installation

### Prerequisites

- Ubuntu 20.04+ (or similar Linux distribution)
- Python 3.10 or higher
- pip and venv

### Install from source

```bash
git clone https://github.com/USERNAME/yctl.git
cd yctl
pip install -e .
```

### Verify installation

```bash
yctl --help
```

## 🚀 Quick Start

### 1. Check System Health

```bash
yctl doctor
```

Verifies Python version, GPU/CUDA availability, and development tools.

### 2. Initialize a New Project

```bash
# NLP project
yctl init nlp sentiment-analyzer

# Computer Vision project
yctl init cv image-classifier

# Machine Learning project
yctl init ml house-price-prediction

# Research project
yctl init research novel-architecture
```

### 3. Inspect a Dataset

```bash
yctl inspect data/train.csv
```

Get comprehensive insights including:
- Dataset statistics and memory usage
- Missing values analysis
- Data quality issues
- Preprocessing suggestions
- Model recommendations

### 4. Analyze an AI Idea

```bash
yctl think "sentiment analysis for customer reviews"
```

Receive expert guidance on:
- Feasibility and complexity assessment
- Step-by-step roadmap
- Recommended datasets and models
- Required tools and libraries
- Learning resources

## 📚 Commands

### `yctl init`

Initialize a new AI/ML project with best practices.

```bash
yctl init <project_type> <project_name> [OPTIONS]
```

**Project Types:**
- `nlp` - Natural Language Processing
- `cv` - Computer Vision
- `ml` - Machine Learning
- `research` - Research Projects

**Options:**
- `--skip-venv` - Skip virtual environment creation

**Example:**
```bash
yctl init nlp sentiment-analyzer
cd sentiment-analyzer
source venv/bin/activate
pip install -r requirements.txt
```

### `yctl inspect`

Inspect and analyze datasets comprehensively.

```bash
yctl inspect <dataset_path> [OPTIONS]
```

**Supported Formats:** CSV, Excel (.xlsx, .xls), JSON, Parquet

**Options:**
- `--sample` - Display sample rows from the dataset

**Example:**
```bash
yctl inspect data/train.csv
```

### `yctl doctor`

Check system health for AI/ML development.

```bash
yctl doctor
```

Verifies:
- Python version (3.10+ recommended)
- pip and venv availability
- GPU detection (NVIDIA)
- CUDA status and version
- Common development tools

### `yctl think`

Analyze an AI project idea and get expert recommendations.

```bash
yctl think "<your_idea>"
```

**Example:**
```bash
yctl think "object detection for autonomous driving"
```

## 🏗️ Project Structure

When you create a project with `yctl init`, you get a well-organized structure:

```
sentiment-analyzer/
├── data/
│   ├── raw/              # Raw datasets
│   └── processed/        # Preprocessed data
├── notebooks/            # Jupyter notebooks
├── src/
│   ├── models/          # Model architectures
│   ├── preprocessing/   # Data preprocessing
│   ├── utils/           # Utility functions
│   └── train.py         # Main training script
├── tests/               # Unit tests
├── configs/             # Configuration files
├── outputs/
│   ├── models/          # Saved models
│   └── logs/            # Training logs
├── venv/                # Virtual environment
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── .gitignore          # Git ignore rules
```

## 💡 Usage Examples

### Complete NLP Workflow

```bash
# 1. Check system
yctl doctor

# 2. Analyze idea
yctl think "sentiment analysis for movie reviews"

# 3. Create project
yctl init nlp movie-sentiment

# 4. Setup
cd movie-sentiment
source venv/bin/activate
pip install -r requirements.txt

# 5. Inspect data
yctl inspect ../data/reviews.csv

# 6. Train
python src/train.py --data data/processed/train.csv --epochs 10
```

### Quick Dataset Analysis

```bash
# Inspect multiple datasets
yctl inspect data/train.csv
yctl inspect data/test.csv
yctl inspect data/validation.csv
```

## 🎯 Best Practices

- **Always activate virtual environment** before working on projects
- **Use `yctl doctor`** before starting new projects
- **Inspect datasets** before training to understand data quality
- **Track experiments** with wandb or tensorboard
- **Version control** your code and configurations
- **Write tests** for critical components

## 🛠️ Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=yctl tests/
```

### Contributing

We welcome all contributions! Please check out our [Contributing Guide (CONTRIBUTING.md)](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [NumPy](https://numpy.org/) - Numerical computing
- [Scikit-learn](https://scikit-learn.org/) - Machine learning utilities

## 📧 Support

- Issues: [GitHub Issues](https://github.com/Youssef-Ai1001/yctl-cli/issues)
- Discussions: [GitHub Discussions](https://github.com/USERNAME/yctl/discussions)

---

**Made with ❤️ for AI Engineers**
