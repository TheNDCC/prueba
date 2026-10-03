# AGENTS.md

Utilidad de escritorio en Python para "Pollos Asados KM9" (Nicaragua). Procesa
reportes de ventas en CSV/Excel y genera salidas formateadas con GUI de Tkinter.
Layout plano, sin paquete raíz.

## Archivos y punto de entrada

| Archivo         | Qué hace                                                                                                                       | Entrada                                                                                          | Salida                                              |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `peya.py`       | Procesa `orderDetails` de PedidosYa: desglosa artículos, genera Excel formateado e imagen JPG de la tabla.                      | CSV/XLS/XLSX con columnas `Nro de pedido`, `Fecha del pedido`, `Artículos` (`Estado del pedido` opcional). | `<base>_procesado.xlsx` + `<base>_procesado.jpg` junto al input. |
| `promicsyst.py` | Limpia Excels de Promicsyst: elimina `Almacén`/`Creado por`/`Nota` y separa la última columna en `Producto` + `Diferencia`.     | XLSX.                                                                                            | `<base>_limpio.xlsx`.                               |
| `prueba.py`     | Corrector de precios: unifica filas SALE con el último precio PURCHASE por producto y reformatea fechas a `YYYY-MM-DD HH:MM`.   | CSV/XLS/XLSX con columnas `Fecha`, `Tipo`, `Producto`, `UNI`.                                    | Ruta elegida por el usuario.                        |

`prueba.py` está sin rastrear en git — no se empaqueta ni se distribuye.

## Cómo ejecutar

- Linux: `./correr.sh`. Activa `.venv` (o `.env`/`env`) si existe, después lanza `peya.py`.
- Windows: `correr.bat` ejecuta `peya.exe` si está presente; si no, indica que hay que compilarlo.
- Manual (cualquier plataforma): `python3 peya.py` / `python3 promicsyst.py` / `python3 prueba.py`. Cada script abre su propia ventana independiente.

No hay un `main` compartido: cada archivo es un ejecutable autónomo con su `if __name__ == "__main__":`.

## Dependencias

`pip install -r requirements.txt`. Versiones fijadas en ese archivo: pandas 2.3.3,
openpyxl 3.1.5, matplotlib 3.10.7, Pillow 12.0.0, numpy 2.4.1, et_xmlfile,
python-dateutil, pytz, six, tzdata.

No hay dependencias de desarrollo, lint ni formato declaradas en el repositorio.

## Convenciones del proyecto

- UI y mensajes al usuario **siempre en español**. Moneda `C$` (Córdoba nicaragüense).
- Toda acción informa al usuario con `messagebox.showinfo` / `showerror` / `showwarning`. Nunca se ejecuta en silencio.
- En `peya.py`, el backend de matplotlib es **Agg** (`matplotlib.use("Agg")` antes de `import matplotlib.pyplot`) para que el binario funcione sin display.
- Para agregar o ajustar productos del menú, editar el dict `PRECIOS` en `peya.py:41`. La búsqueda de precios usa `_normalizar_texto()` (NFD + strip de diacríticos) con coincidencia bidireccional por subcadena — no hay archivo de configuración externo.
- Los diálogos de selección de archivo abren por defecto en `~/Downloads`, con fallback a `~/Descargas`.
- La salida se escribe **junto al archivo de entrada**, no en `output/` (aunque `promicsyst.py` define `output_dir`, ya no se usa para la ruta final).
- Estilo de Excel: encabezado con relleno `#4472C4` y texto blanco en negrita; fila TOTAL con relleno `#D9E2F3` en negrita. Constantes y anchos definidos al inicio de `peya.py`.

## Lo que NO hay en el repo

- Sin tests, sin pytest, sin CI, sin pre-commit, sin config de lint/format (no hay `pyproject.toml`, `ruff.toml` ni `mypy.ini` en el árbol de trabajo).
- No es un monorepo — todos los scripts viven en el raíz.
- No hay política documentada de ramas, PRs ni releases; los commits del historial están en español.
- No hay instrucciones de empaquetado versionadas aquí — el `.exe` se produce con scripts `build.bat` / `build_peya.spec` que se mantienen fuera de este archivo.