import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# ==========================
#  LISTA DE PRECIOS
# ==========================

PRECIOS = {
    "pollo asado entero": 300,
    "pollo asados entero": 300,   # variante que a veces trae PedidosYa
    "pollo asado medio": 150,
    "medio pollo asado": 150,
    "pollo rostizado entero": 340,
    "medio rostizado": 170,
    "puyazo": 200,
    "churrasco": 200,
    "cerdo asado": 160,
    "carne asada": 180,

    "gaseosa 355 ml": 30,

    "gaseosa 2 lt": 70,
    "coca cola 2lt": 70,

    "gaseosa 3 lt": 90,
    "coca cola 3lt": 90,

    "nachos supremos de res": 150,
}

# ==========================
#  FUNCIONES BASE
# ==========================


def find_price(name: str):
    """Devuelve el precio según el nombre del producto usando coincidencia parcial."""
    n = str(name).lower()
    for clave, valor in PRECIOS.items():
        if clave in n:
            return valor
    return None


def procesar_archivo(file_path: str):
    """Lee el archivo de PedidosYa y genera un Excel con la tabla Detalle."""

    # 1) Leer CSV o Excel según extensión
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path, engine="python")
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
        else:
            messagebox.showerror(
                "Error", f"Tipo de archivo no soportado: {ext}")
            return
    except Exception as e:
        messagebox.showerror("Error al leer el archivo", str(e))
        return

    # 2) Verificar que existan las columnas que necesitamos
    columnas_necesarias = ["Nro de pedido", "Fecha del pedido", "Artículos"]
    for col in columnas_necesarias:
        if col not in df.columns:
            messagebox.showerror(
                "Error",
                f"En el archivo falta la columna: '{col}'.\n"
                "Verificá que el archivo sea el orderDetails original de PedidosYa."
            )
            return

    # Estado del pedido es opcional (si no está, dejamos columna vacía)
    tiene_estado = "Estado del pedido" in df.columns

    filas = []

    for _, fila in df.iterrows():
        pedido = fila.get("Nro de pedido", "")
        fecha = fila.get("Fecha del pedido", "")
        estado = fila.get("Estado del pedido", "") if tiene_estado else ""
        articulos = fila.get("Artículos", "")

        if not isinstance(articulos, str) or not articulos.strip():
            continue

        # Ejemplo: "1 Pollo asado entero, 2 Pollo asado medio"
        items = [x.strip() for x in articulos.split(",") if x.strip()]

        for item in items:
            partes = item.split(" ", 1)
            try:
                cantidad = int(partes[0])
                nombre = partes[1].strip()
            except Exception:
                cantidad = 1
                nombre = item.strip()

            precio = find_price(nombre)
            subtotal = cantidad * precio if precio is not None else None

            filas.append({
                "Numero de pedido": pedido,
                "Fecha": fecha,
                "Producto": nombre.title(),
                "Cantidad": cantidad,
                "Precio unitario (C$)": precio,
                "Subtotal (C$)": subtotal,
                "Entregado": estado,
            })

    if not filas:
        messagebox.showwarning(
            "Sin datos",
            "No se encontraron artículos para procesar en este archivo."
        )
        return

    detalle = pd.DataFrame(filas)

    # 3) Guardar a Excel (solo hoja Detalle, como en tu imagen)
    base, ext = os.path.splitext(file_path)
    output_path = base + "_procesado.xlsx"

    try:
        with pd.ExcelWriter(output_path) as writer:
            detalle.to_excel(writer, index=False, sheet_name="Detalle")
    except Exception as e:
        messagebox.showerror("Error al guardar el Excel", str(e))
        return

    # 4) Calcular total general
    total = detalle["Subtotal (C$)"].sum(skipna=True)

    messagebox.showinfo(
        "Proceso completado",
        f"Archivo generado:\n{output_path}\n\n"
        f"Total general: C$ {total:.2f}"
    )


# ==========================
#  INTERFAZ GRÁFICA
# ==========================

def seleccionar_y_procesar():
    file_path = filedialog.askopenfilename(
        title="Seleccionar orderDetails de PedidosYa",
        filetypes=(
            ("Archivos CSV", "*.csv"),
            ("Archivos Excel", "*.xlsx;*.xls"),
            ("Todos los archivos", "*.*"),
        )
    )
    if file_path:
        procesar_archivo(file_path)


def main():
    root = tk.Tk()
    root.title("Procesar reportes PedidosYa - Pollos Asados KM9")
    root.geometry("500x220")

    label = tk.Label(
        root,
        text=(
            "Procesador de reportes PedidosYa\n\n"
            "1. Seleccioná el archivo orderDetails (.csv o .xlsx)\n"
            "2. Se generará un Excel con la tabla Detalle:\n"
            "   Número de pedido, Fecha, Producto, Cantidad,\n"
            "   Precio unitario, Subtotal y Entregado."
        ),
        justify="left"
    )
    label.pack(pady=15)

    boton = tk.Button(
        root,
        text="Seleccionar archivo y procesar",
        command=seleccionar_y_procesar,
        width=35,
        height=2
    )
    boton.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
