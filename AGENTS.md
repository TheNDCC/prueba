# AGENTS.md - Development Guidelines

## Project Overview

This is a Python desktop application for processing restaurant sales data from PedidosYa (delivery platform) and Promicsyst (inventory system). It generates Excel reports with pricing and order details.

## Project Structure

```
/home/nelson/Documents/repo/prueba
├── prueba.py       # Main app: process PedidosYa orderDetails CSV/Excel
├── Prueba2.py      # Process Promicsyst CSV files
├── Prueba3.py      # Process Promicsyst Excel files
├── requirements.txt
├── correr.sh       # Run script (activates venv, runs prueba.py)
├── correr.bat      # Windows run script
├── csv/            # Input CSV files
└── output/         # Generated reports
```

## Dependencies

- pandas
- openpyxl
- numpy
- python-dateutil
- pytz
- tkinter (built-in)

Install: `pip install -r requirements.txt`

---

## Build & Run Commands

### Running the Application

```bash
# Using the shell script (recommended)
./correr.sh

# Direct execution
python3 prueba.py       # PedidosYa processor
python3 Prueba2.py      # Promicsyst CSV processor
python3 Prueba3.py      # Promicsyst Excel processor
```

### Virtual Environment

The project uses `.venv` (Python 3.12). Activate with:
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Testing

**No test framework is currently configured.** To add tests:

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run a single test file
pytest test_file.py

# Run a single test function
pytest test_file.py::test_function_name

# Run tests matching a pattern
pytest -k "test_name_pattern"
```

### Linting & Formatting

**No linter/formatter configured.** Recommended setup:

```bash
# Install ruff (fast linter + formatter)
pip install ruff

# Run linter
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Check types (requires pyright or mypy)
pip install pyright
pyright .
```

---

## Code Style Guidelines

### General Principles

- Keep functions small and focused (single responsibility)
- Use explicit variable names (avoid cryptic abbreviations)
- Handle errors gracefully with try/except blocks
- Use type hints for function parameters and return values

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | snake_case | `procesar_archivo`, `find_price` |
| Variables | snake_case | `file_path`, `output_rows` |
| Constants | UPPER_SNAKE_CASE | `PRECIOS`, `CSV_DIR` |
| Classes | PascalCase | (not used in this project) |
| File names | snake_case | `prueba.py`, `Prueba2.py` |

### Import Order

```python
# 1. Standard library
import os
import re
import csv

# 2. Third-party packages
import pandas as pd

# 3. GUI frameworks (after other imports)
import tkinter as tk
from tkinter import filedialog, messagebox
```

### Type Hints

Use type hints for all function signatures:

```python
# Good
def find_price(name: str) -> int | None:
    ...

def procesar_archivo(file_path: str) -> None:
    ...

# Avoid
def find_price(name):
    ...
```

### Error Handling

Always show user-friendly error messages via `messagebox`:

```python
try:
    df = pd.read_excel(file_path)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
    return
```

For critical errors that should stop execution, use `messagebox.showerror` then `return` or `sys.exit(1)`.

### GUI Patterns

- Use `tk.Tk()` as main window
- Keep `root.mainloop()` at the end of `main()`
- Use `filedialog` for file selection
- Use `messagebox` for errors, warnings, and info
- Center window or set reasonable size (e.g., `root.geometry("550x250")`)

### Constants

Define configuration constants at module level:

```python
# Good
output_dir = "output"
csv_dir = "csv/"
PRECIOS = {"pollo asado": 300}

# Avoid magic strings/values scattered in code
```

### Documentation

Add docstrings for public functions:

```python
def find_price(name: str) -> int | None:
    """Devuelve el precio según el nombre del producto usando coincidencia parcial."""
    ...
```

### File Paths

Use `os.path` for cross-platform compatibility:

```python
output_path = os.path.join(output_dir, "resultado.xlsx")
file_path = os.path.splitext(input_file_path)[0] + "_limpio.xlsx"
```

### Data Processing with Pandas

```python
# Read files
df = pd.read_csv(file_path, engine="python")  # for CSV
df = pd.read_excel(file_path)                  # for Excel

# Write files
df.to_excel(output_file, index=False, sheet_name="Detalle")

# Iterate over rows
for _, row in df.iterrows():
    ...
```

---

## Adding New Features

1. Create a new Python file following naming convention (`new_feature.py`)
2. Add dependencies to `requirements.txt` if needed
3. Use the same code style as existing files
4. Test locally before committing

---

## Common Issues

- **CSV delimiter**: Some files use semicolon (`;`) - use `delimiter=";"` in `csv.reader`
- **Empty cells**: Check with `pd.isna()` or compare to `"nan"` as string
- **HTML tags**: Strip `<p>` and `</p>` tags from cell content
- **Encoding**: Always use `encoding="utf-8"` for text files
