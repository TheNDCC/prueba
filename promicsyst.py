import os
import re
import pandas as pd

# GUI
import tkinter as tk
from tkinter import filedialog, messagebox

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
        messagebox.showwarning("Sin archivo", "Selecciona un archivo Excel.")
        return

    try:
        df = pd.read_excel(input_file_path)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
        return

    if df.empty:
        messagebox.showwarning("Archivo vacío", "El archivo no contiene datos.")
        return

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

    output_file = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(input_file_path))[0] + "_limpio.xlsx"
    )

    df_out.to_excel(output_file, index=False)

    messagebox.showinfo(
        "Proceso completado",
        f"Archivo generado correctamente:\n{output_file}\n\n"
        f"Filas procesadas: {len(df_out)}"
    )


# =====================
# GUI
# =====================
def seleccionar_archivo():
    global selected_file
    selected_file = filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=(("Archivos Excel", "*.xlsx"),)
    )

    if selected_file:
        lbl_archivo.config(
            text=f"Archivo seleccionado:\n{os.path.basename(selected_file)}"
        )


def ejecutar():
    if not selected_file:
        messagebox.showwarning("Sin archivo", "Selecciona un archivo primero.")
        return
    procesar_archivo_excel(selected_file)


def main():
    global lbl_archivo

    root = tk.Tk()
    root.title("FixPromicsyst - Excel")
    root.geometry("550x260")

    instrucciones = (
        "Instrucciones:\n"
        "1) Selecciona el archivo Excel original de Promicsyst.\n"
        "2) El sistema separará productos y diferencias.\n"
        "3) Se generará un Excel limpio en la carpeta 'output/'."
    )

    tk.Label(root, text=instrucciones, justify="left").pack(pady=10)

    lbl_archivo = tk.Label(root, text="Ningún archivo seleccionado")
    lbl_archivo.pack(pady=5)

    tk.Button(root, text="Seleccionar archivo Excel",
              command=seleccionar_archivo).pack(pady=5)

    tk.Button(
        root,
        text="Procesar archivo",
        command=ejecutar,
        bg="#4CAF50",
        fg="white",
        width=20
    ).pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
