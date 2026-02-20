# yctl  
**Personal AI Engineer CLI Tool for Ubuntu**

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)  
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Command-line tool to streamline AI/ML development workflows with best practices.

---

## ✨ Features

- 🚀 Initialize AI/ML projects in seconds  
- 🔍 Smart dataset inspection  
- 🏥 System diagnostics (Python / CUDA / GPU)  
- 💡 AI idea feasibility analyzer  

---

## 📦 Installation

### Requirements
- Ubuntu 20.04+
- Python 3.10+
- pip + venv

### Install

```bash
git clone https://github.com/Youssef-Ai1001/yctl-cli.git
cd yctl-cli
pip install -e .
```

Verify installation:

```bash
yctl --help
```

---

## 🚀 Quick Usage

### System Check

```bash
yctl doctor
```

---

### Create Project

```bash
yctl init nlp sentiment-analyzer
yctl init cv image-classifier
yctl init ml house-price
yctl init research new-architecture
```

---

### Inspect Dataset

```bash
yctl inspect data/train.csv
```

Supported formats: CSV, Excel, JSON, Parquet

---

### Analyze AI Idea

```bash
yctl think "sentiment analysis for customer reviews"
```

---

## 🏗️ Generated Project Structure

```
project-name/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── models/
│   ├── preprocessing/
│   ├── utils/
│   └── train.py
├── tests/
├── configs/
├── outputs/
├── venv/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠 Troubleshooting

### CUDA Not Detected

```bash
nvidia-smi
sudo ubuntu-drivers autoinstall
reboot
```

Docs:
- https://docs.nvidia.com/cuda/
- https://pytorch.org/get-started/locally/

---

### OpenCV libGL Error

```bash
sudo apt update
sudo apt install -y libgl1
```

---

### Virtual Environment Permission Error

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

---

## 🧪 Development

```bash
pip install -e ".[dev]"
pytest tests/
pytest --cov=yctl tests/
```

---

## 📄 License

MIT License

---

## 📧 Support

- Issues: https://github.com/Youssef-Ai1001/yctl-cli/issues  
- Discussions: https://github.com/Youssef-Ai1001/yctl-cli/discussions  

---

**Built for AI Engineers 🚀**
