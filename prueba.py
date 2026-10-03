import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def corregir_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos CSV y Excel", "*.csv *.xlsx *.xls")]
    )

    if not archivo:
        return

    try:
        if archivo.endswith('.csv'):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        # Filtrar filas con fechas inválidas (Summary, imágenes, etc.)
        def es_fecha_valida(valor):
            try:
                pd.to_datetime(valor, format='%d/%m/%Y %H:%M')
                return True
            except:
                return False

        df = df[df['Fecha'].apply(es_fecha_valida)].copy()

        # 1. Convertir fechas a YYYY-MM-DD HH:MM
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y %H:%M')
        df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d %H:%M')

        # NormalizarTipo (minúsculas y sin espacios)
        df["Tipo"] = df["Tipo"].astype(str).str.strip().str.lower()

        # Normalizar nombre de productos (colapsar espacios múltiples)
        df["Producto"] = df["Producto"].str.replace(r'\s+', ' ', regex=True).str.strip()

        # Identificar columna uni/UNI (case-insensitive)
        col_uni = [c for c in df.columns if c.lower() == 'uni'][0]

        # 2. Redondear precios a 2 decimales
        df[col_uni] = (
            df[col_uni]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        ).round(2)

        # 3. Obtener últimos precios desde PURCHASE (usando drop_duplicates)
        compras = df[df["Tipo"] == "purchase"]
        compras_unicas = compras.drop_duplicates(subset=["Producto"], keep="last")
        precios_purchase = dict(zip(compras_unicas["Producto"], compras_unicas[col_uni]))

        # 4. Corregir precios en SALE
        for i, row in df.iterrows():
            if row["Tipo"] == "sale":
                producto = row["Producto"]
                if producto in precios_purchase:
                    df.at[i, col_uni] = precios_purchase[producto]

        # Guardar
        guardar = filedialog.asksaveasfilename(
            title="Guardar archivo corregido",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )

        if guardar:
            df.to_excel(guardar, index=False)
            messagebox.showinfo("Éxito", "Archivo corregido correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Corrector de precios UNI")
ventana.geometry("350x180")
ventana.resizable(False, False)

# Título
titulo = tk.Label(
    ventana,
    text="Corregir precios SALE",
    font=("Arial", 14, "bold")
)
titulo.pack(pady=20)

# Botón
boton = tk.Button(
    ventana,
    text="Seleccionar archivo Excel",
    command=corregir_archivo,
    width=25,
    height=2
)
boton.pack(pady=20)

# Ejecutar interfaz
ventana.mainloop()