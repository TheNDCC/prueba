# Instrucciones de uso
# 1️⃣ Ejecutar: python FixPromicsyst.py
# 2️⃣ En la ventana, hacer clic en "Seleccionar archivo CSV".
# 3️⃣ Elegir el archivo CSV de Promicsyst.
# 4️⃣ Se generará el CSV limpio en la carpeta "output/".

import os
import re
import csv

# === NUEVO: imports para GUI ===
import tkinter as tk
from tkinter import filedialog, messagebox

csv_dir = "csv/"
output_dir = "output/"

# === Verificar existencia de carpetas ===
os.makedirs(csv_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# =========================================
# FUNCIÓN QUE USA TU LÓGICA ORIGINAL (1 archivo)
# =========================================


def procesar_archivo(input_file_path: str):
    if not input_file_path:
        messagebox.showwarning(
            "Sin archivo", "Primero selecciona un archivo CSV.")
        return

    file_name = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_dir, file_name)

    with open(input_file_path, newline="", encoding="utf-8") as csvfile:
        # Usar punto y coma como delimitador
        csv_rows = list(csv.reader(csvfile, delimiter=";", quotechar='"'))
        output_csv = []

        # Verificar que hay datos
        if len(csv_rows) == 0:
            msg = f"⚠️ El archivo {file_name} está vacío."
            print(msg)
            messagebox.showwarning("Archivo vacío", msg)
            return

        # Encabezado original
        header = csv_rows[0]
        # Buscar la columna que contiene los productos (normalmente la última)
        new_header = header[:-1] + ["Producto", "Diferencia"]
        output_csv.append(new_header)

        # Procesar filas de datos
        for row in csv_rows[1:]:
            # Saltar filas vacías
            if not row or len(row) == 0:
                continue

            # Limpiar etiquetas HTML o espacios
            row = [col.replace("<p>", "").replace(
                "</p>", "").strip() for col in row]

            # Buscar la columna que contiene los productos con paréntesis
            product_column_index = -1
            for i, col in enumerate(row):
                if re.search(r"\(([-0-9.]+)\)", col):
                    product_column_index = i
                    break

            # Si no encontramos productos, saltar esta fila
            if product_column_index == -1:
                continue

            # Separar productos por salto de línea
            for product_line in row[product_column_index].split("\n"):
                product_line = product_line.strip()
                if not product_line:
                    continue

                # Extraer cantidad (diferencia)
                match = re.search(r"\(([-0-9.]+)\)", product_line)
                if match:
                    try:
                        diferencia = float(match.group(1))
                    except ValueError:
                        diferencia = 0.0
                else:
                    diferencia = 0.0

                # Nombre del producto
                product_name = re.sub(r"\(.*?\)", "", product_line).strip()

                # Construir fila limpia
                clean_row = row[:product_column_index] + \
                    [product_name, diferencia]
                output_csv.append(clean_row)

    # === Guardar archivo limpio ===
    with open(output_file_path, mode="w", newline="", encoding="utf-8") as new_file:
        writer = csv.writer(new_file, delimiter=";")
        writer.writerows(output_csv)

    print(f"✅ Archivo procesado y guardado en {output_file_path}")
    print(f"📊 Total de filas procesadas: {len(output_csv) - 1}")

    messagebox.showinfo(
        "Proceso completado",
        f"✅ Archivo procesado y guardado en:\n{output_file_path}\n\n"
        f"📊 Total de filas procesadas: {len(output_csv) - 1}"
    )

# ======================
#  INTERFAZ GRÁFICA GUI
# ======================


selected_file = None  # variable global para guardar el archivo elegido


def seleccionar_archivo():
    global selected_file
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    if file_path:
        selected_file = file_path
        lbl_archivo.config(
            text=f"Archivo seleccionado:\n{os.path.basename(file_path)}")


def ejecutar_proceso():
    if not selected_file:
        messagebox.showwarning(
            "Sin archivo", "Primero selecciona un archivo CSV.")
        return
    procesar_archivo(selected_file)


def main():
    global lbl_archivo

    root = tk.Tk()
    root.title("FixPromicsyst - Procesar CSV")
    root.geometry("550x250")

    instrucciones = (
        "Instrucciones:\n"
        "1) Haz clic en 'Seleccionar archivo CSV'.\n"
        "2) Elige el archivo CSV original de Promicsyst.\n"
        "3) Se generará el archivo limpio en la carpeta 'output/'."
    )

    lbl_info = tk.Label(root, text=instrucciones, justify="left")
    lbl_info.pack(pady=10)

    lbl_archivo = tk.Label(root, text="Ningún archivo seleccionado")
    lbl_archivo.pack(pady=5)

    btn_sel = tk.Button(root, text="Seleccionar archivo CSV",
                        command=seleccionar_archivo)
    btn_sel.pack(pady=5)

    btn_proc = tk.Button(
        root,
        text="Procesar archivo",
        command=ejecutar_proceso,
        bg="#4CAF50",
        fg="white",
        width=20
    )
    btn_proc.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
