#!/usr/bin/env bash
set -euo pipefail

# Cambiar al directorio del script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir" || exit 1

# Intentar activar un entorno virtual común si existe
if [ -f ".env/bin/activate" ]; then
  # shellcheck disable=SC1091
  . .env/bin/activate
elif [ -f ".venv/bin/activate" ]; then
  . .venv/bin/activate
elif [ -f "env/bin/activate" ]; then
  . .env/bin/activate
fi

# Seleccionar intérprete Python disponible
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "No se encontró Python en PATH. Instale Python o active un entorno virtual."
  exit 1
fi

# Seleccionar script a ejecutar: peya (por defecto) | promicsyst | prueba
SCRIPT="${1:-peya}"
shift 2>/dev/null || true

case "$SCRIPT" in
  peya)       FILE="peya.py" ;;
  promicsyst) FILE="promicsyst.py" ;;
  prueba)     FILE="prueba.py" ;;
  *)
    echo "Script no reconocido: $SCRIPT"
    echo "Uso: $0 [peya|promicsyst|prueba]"
    exit 1
    ;;
esac

if [ ! -f "$FILE" ]; then
  echo "No se encontró $FILE en $script_dir"
  exit 1
fi

# Ejecutar el programa (pasa cualquier argumento recibido al script)
"$PY" "$FILE" "$@"

# Pausa similar a "pause" de Windows
read -n1 -rsp $'Presione cualquier tecla para continuar...\n' || true
