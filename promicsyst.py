import os
import re

# GUI
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd

# =====================
# CONFIGURACIÓN
# =====================
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

selected_file = None


# =====================
# PROCESAMIENTO
# =====================
def procesar_archivo_excel(input_file_path: str):
    if not input_file_path:
        # Abrir diálogo en carpeta Downloads/Descargas
        downloads_path = os.path.expanduser("~/Downloads")
        if not os.path.exists(downloads_path):
            downloads_path = os.path.expanduser("~/Descargas")

        selected = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            initialdir=downloads_path,
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")),
        )
        if not selected:
            messagebox.showwarning("Sin archivo", "Selecciona un archivo Excel.")
            return
        input_file_path = selected

    try:
        df = pd.read_excel(input_file_path)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
        return

    if df.empty:
        messagebox.showwarning("Archivo vacío", "El archivo no contiene datos.")
        return

    # Leemos el dataframe y eliminamos columnas no deseadas por nombre
    # Eliminar columnas: "Almacén", "Creado por", "Nota" si existen
    cols_to_drop = [c for c in ["Almacén", "Creado por", "Nota"] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    # Usamos todas las columnas excepto la última
    base_columns = list(df.columns[:-1])
    producto_col = df.columns[-1]

    output_rows = []

    for _, row in df.iterrows():
        raw_cell = str(row[producto_col])

        if not raw_cell or raw_cell == "nan":
            continue

        # Limpiar HTML
        raw_cell = raw_cell.replace("<p>", "").replace("</p>", "").strip()

        for product_line in raw_cell.split("\n"):
            product_line = product_line.strip()
            if not product_line:
                continue

            match = re.search(r"\(([-0-9.]+)\)", product_line)
            diferencia = float(match.group(1)) if match else 0.0
            producto = re.sub(r"\(.*?\)", "", product_line).strip()
            new_row = list(row[base_columns]) + [producto, diferencia]
            output_rows.append(new_row)

    # Crear DataFrame final
    final_columns = base_columns + ["Producto", "Diferencia"]
    df_out = pd.DataFrame(output_rows, columns=final_columns)

    # Guardamos en la misma carpeta de búsqueda si fue encontrada en Descargas/Downloads
    # Construimos ruta de salida en el mismo directorio que el input
    input_dir = os.path.dirname(input_file_path)
    output_file = os.path.join(
        input_dir,
        os.path.splitext(os.path.basename(input_file_path))[0] + "_limpio.xlsx",
    )

    df_out.to_excel(output_file, index=False)

    messagebox.showinfo(
        "Proceso completado",
        f"Archivo generado correctamente:\n{output_file}\n\nFilas procesadas: {len(df_out)}",
    )
    # Autoajustar ancho de columnas en Excel resultante (opcional con openpyxl)
    try:
        from openpyxl import load_workbook

        wb = load_workbook(output_file)
        ws = wb.active
        for col_cells in ws.columns:
            max_length = 0
            for cell in col_cells:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            col_letter = col_cells[0].column_letter
            ws.column_dimensions[col_letter].width = max(max_length + 2, 10)
        wb.save(output_file)
    except Exception:
        # Si openpyxl no disponible o fallo, ignorar
        pass


# =====================
# GUI
# =====================
def seleccionar_archivo():
    global selected_file
    downloads_path = os.path.expanduser("~/Downloads")
    if not os.path.exists(downloads_path):
        downloads_path = os.path.expanduser("~/Descargas")

    selected_file = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        initialdir=downloads_path,
        filetypes=(("Archivos Excel", "*.xlsx"),),
    )

    if selected_file:
        lbl_archivo.config(text=f"Archivo seleccionado:\n{os.path.basename(selected_file)}")


def ejecutar():
    if not selected_file:
        messagebox.showwarning("Sin archivo", "Selecciona un archivo primero.")
        return
    procesar_archivo_excel(selected_file if selected_file else "")


def main():
    global lbl_archivo

    root = tk.Tk()
    root.title("FixPromicsyst - Excel")
    root.geometry("550x260")

    instrucciones = (
        "Instrucciones:\n"
        "1) El sistema buscará automáticamente en Descargas/Downloads.\n"
        "2) Si no lo encuentra, podrás seleccionar el archivo manualmente.\n"
        "3) El sistema separará productos y diferencias.\n"
        "4) Se generará un Excel limpio en la misma carpeta del archivo original."
    )

    tk.Label(root, text=instrucciones, justify="left").pack(pady=10)

    lbl_archivo = tk.Label(root, text="Ningún archivo seleccionado")
    lbl_archivo.pack(pady=5)

    tk.Button(root, text="Seleccionar archivo Excel", command=seleccionar_archivo).pack(pady=5)

    tk.Button(
        root,
        text="Procesar archivo",
        command=ejecutar,
        bg="#4CAF50",
        fg="white",
        width=20,
    ).pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
