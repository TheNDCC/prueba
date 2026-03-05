# AGENTS.md - Development Guidelines

**Project**: Utilidades de Km9  
**Description**: Python desktop application for processing restaurant sales data from PedidosYa and Promicsyst. Generates Excel reports with pricing and order details.

## Project Structure

```
peya.py           # Main app: process PedidosYa orderDetails CSV/Excel
promicsyst.py     # Process Promicsyst Excel files
requirements.txt  # Python dependencies
correr.sh         # Run script (activates venv)
output/           # Generated reports
csv/              # Input CSV files (if needed)
```

**Dependencies**: pandas, openpyxl, numpy, matplotlib, Pillow, python-dateutil, pytz, tkinter (built-in)

Install: `pip install -r requirements.txt`

---

## Build & Run Commands

```bash
# Create and activate virtual environment
python3 -m venv .venv && source .venv/bin/activate
# or: ./correr.sh

# Run applications
python3 peya.py         # PedidosYa processor
python3 promicsyst.py   # Promicsyst processor

# Linting
ruff check .           # Lint all files
ruff check peya.py     # Lint specific file
ruff check --fix .     # Fix linting issues
ruff format .          # Format code

# Type checking
mypy .                 # Type check all
mypy peya.py          # Type check specific file

# Run tests
pytest                           # All tests
pytest test_file.py              # Single test file
pytest tests/test_peya.py::test_function_name  # Single test
pytest -k "pattern"             # Match test names
```

---

## Code Style Guidelines

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | snake_case | `procesar_archivo` |
| Variables | snake_case | `file_path` |
| Constants | UPPER_SNAKE | `PRECIOS` |
| Files | snake_case | `peya.py` |
| Classes | PascalCase | `ExcelFormatter` |

### Import Order

```python
# 1. Standard library
import io, os, re

# 2. Third-party packages
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

# 3. GUI frameworks
import tkinter as tk
from tkinter import messagebox, filedialog
```

### Type Hints & Docstrings

```python
def find_price(name: str) -> int | None:
    """Find price for a product name."""
    return PRECIOS.get(name.lower())
```

### Comments

- **Explain "why", not "what"**: Code describes what it does; comments explain business logic decisions
- Use Spanish comments for business logic (since this is a local restaurant utility)
- Use English for technical explanations when needed

```python
# Precio especial de Fin de Semana - no está en la lista oficial
# This matches "pollos asados" (plural) variant from PedidosYa exports
```

### Error Handling

```python
try:
    df = pd.read_excel(file_path)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo leer:\n{e}")
    return
```

- Always show user-friendly error messages in Spanish via `messagebox`
- Return early on failure to prevent cascading errors
- Log technical details to console for debugging

### Debugging

- Use `print()` for quick debugging (acceptable for this project)
- For complex issues, add temporary debug output before return statements
- Remove debug code before committing
- Test with sample files from `csv/` directory when available

---

## Formatting & Linting

### Python

**Tools**: ruff, mypy

**Configuration** (add to `pyproject.toml` if needed):

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
```

**Commands**:

```bash
# Lint and fix
ruff check . --fix
ruff format .

# Type check
mypy .
```

### Editor Configuration

**VS Code** (`.vscode/settings.json`):

```json
{
    "python.linting.ruffEnabled": true,
    "python.linting.ruffArgs": ["--extend-ignore=E501"],
    "python.formatting.provider": "ruff",
    "python.analysis.typeCheckingMode": "basic",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

**PyCharm**:
- Enable Ruff as external tool
- Set line length to 100 in code style settings

---

## Project-Specific Guidelines

### Simplicity and Legibility

- **Prefer explicit over implicit**: Clear variable names, avoid clever one-liners
- **Single responsibility**: Each function does one thing well
- **No over-engineering**: This is a utility app, not an enterprise system
- **Maximum function length**: ~50 lines; split longer functions

### GUI with Tkinter

- Use grid or pack layout consistently (don't mix)
- Keep window dimensions fixed unless resizing is necessary
- Use standard tkinter widgets; avoid customtkinter unless justified
- **Always** inform user of success/failure via `messagebox`

```python
# Good pattern
root = tk.Tk()
root.title("App Title")
root.geometry("500x220")
tk.Button(root, text="Procesar", command=funcion).pack()
root.mainloop()

# Bad pattern - no user feedback
funcion()  # Silent execution
```

### Application Architecture

```
┌─────────────────┐     ┌──────────────────┐
│    peya.py     │     │  promicsyst.py   │
│                 │     │                  │
│ - GUI entry    │     │ - GUI entry      │
│ - procesar_    │     │ - procesar_      │
│   archivo()    │     │   archivo_excel()│
│ - find_price() │     │ - Regex parsing  │
│ - formatear_   │     │ - Column cleanup │
│   excel()      │     │                  │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         ▼                       ▼
    [output/]              [output/]
    *_procesado.xlsx       *_limpio.xlsx
```

**Module interconnection**:
- Each processor is independent; no shared state
- Constants (like `PRECIOS`) defined at module level
- Reusable styles defined as module-level constants

### User Experience

- **Auto-search feature**: Check `~/Downloads` and `~/Descargas` automatically
- **Manual fallback**: Allow file selection via dialog if auto-search fails
- **Clipboard integration**: Copy generated tables as images for WhatsApp sharing
- **Clear success messages**: Show output path and summary statistics
- **Warning for partial failures**: Continue processing even if some rows fail

---

## Testing Patterns

### Testing Approach

- **Unit tests**: Test pure functions like `find_price()`, `_parse_articulos()`, `_normalizar_texto()`
- **Integration tests**: Test file I/O with sample CSV/Excel files
- **No browser testing**: This is a desktop app, not web

### Test File Structure

```
tests/
├── __init__.py
├── test_peya.py
└── test_promicsyst.py
```

### Example Test

```python
import pytest
from peya import find_price, _normalizar_texto, _parse_articulos

def test_find_price_exact_match():
    assert find_price("pollo asado entero") == 320
    assert find_price("agua alpina 600 ml") == 30

def test_find_price_partial_match():
    assert find_price("pollo asado") == 320
    assert find_price("nachos supremos de res") == 150

def test_normalizar_texto():
    assert _normalizar_texto("Pollo Asado") == "pollo asado"
    assert _normalizar_texto("Niño") == "nino"

def test_parse_articulos():
    assert _parse_articulos("2 pollo asado") == [(2, "pollo asado")]
    assert _parse_articulos("1 agua") == [(1, "agua")]
```

### Validation by User

- **Confirm before destructive operations**: Not required for this app (read-only processing)
- **Show preview**: Display row count before generating output
- **User confirms output location**: Default to same directory as input

---

## Additional Notes

### Language and Localization

- **UI Language**: Spanish (Mexico/Central America - Córdoba pricing)
- **User-facing messages**: Always in Spanish
- **Code comments**: Spanish for business logic, English for technical notes
- **Currency**: C$ (Córdoba Nicaragüense)

```python
# Good
messagebox.showinfo("Éxito", f"Archivo guardado en: {output_path}")

# Avoid
messagebox.showinfo("Success", f"File saved to: {output_path}")
```

### Database Considerations

- **No database**: This project works with CSV/Excel files only
- **Data persistence**: Output Excel files serve as persistent storage
- **No migrations**: Not applicable

### Security

- **No secrets**: No API keys, passwords, or credentials stored
- **File access**: Only read from user-selected paths
- **Output sandboxing**: Write to user-specified or default output directory
- **Input validation**: Verify file extensions before processing

```python
# Good - validate extension
ext = os.path.splitext(file_path)[1].lower()
if ext not in [".csv", ".xls", ".xlsx"]:
    messagebox.showerror("Error", f"Tipo no soportado: {ext}")

# Good - check column existence
for col in required_columns:
    if col not in df.columns:
        messagebox.showerror("Error", f"Falta columna: {col}")
```

### Performance

- **Chunk large files**: Use `chunksize` for pandas if file > 100MB
- **Lazy evaluation**: Process rows on-demand for large datasets
- **Memory cleanup**: Close workbooks explicitly after use
- **Avoid unnecessary copies**: Use `inplace=True` where safe

```python
# Good - process in chunks for large files
for chunk in pd.read_csv(file_path, chunksize=10000):
    process_chunk(chunk)

# Good - cleanup
wb.close()
plt.close('all')
```

---

## Resources

### Documentation

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [matplotlib non-GUI usage](https://matplotlib.org/stable/tutorials/introductory/usage.html#backends)

### Libraries

- [Ruff - Fast Python linter](https://docs.astral.sh/ruff/)
- [mypy - Static type checker](https://mypy.readthedocs.io/)

### Project Conventions

- **Auto-search paths**: Check `~/Downloads` and `~/Descargas` for input files
- **Output naming**: `{original_name}_procesado.xlsx` or `{original_name}_limpio.xlsx`
- **Excel formatting**: Header row with blue background (#4472C4), bold white text

---

## Adding New Features

1. Create new Python file with snake_case naming
2. Add dependencies to `requirements.txt`
3. Follow code style guidelines
4. Test locally before committing
5. Use `messagebox` to inform user of success/failure
6. Update this AGENTS.md if adding new patterns or tools
