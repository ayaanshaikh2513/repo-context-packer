# repo-context-packer
# 📦 repo-context-packer

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

Turn any local codebase into a clean, token-counted Markdown file ready for **ChatGPT, Claude, Gemini, or local Ollama models** in one command.

## ✨ Features
- **Zero Dependencies:** Runs on pure Python standard library.
- **Smart Filtering:** Automatically skips `node_modules`, `.git`, virtual environments, and binary assets.
- **Visual File Tree:** Generates an ASCII directory map at the top of the prompt so the LLM understands your architecture immediately.
- **Token Estimator:** Calculates approximate token usage on every run.

## 🚀 Quick Start

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/repo-context-packer.git](https://github.com/YOUR_USERNAME/repo-context-packer.git)
cd repo-context-packer

# Pack any project folder
python packer.py /path/to/your/project -o prompt_context.md
```

## 🛠️ CLI Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `path` | Target directory to scan | `.` (Current folder) |
| `-o`, `--output` | Output Markdown file name | `context.md` |
| `--max-kb` | Max file size in KB before skipping | `500` |

## 🤝 Contributing
Pull requests are welcome! Looking for contributors to help add custom `.gitignore` parsing and clipboard auto-copy flags.
