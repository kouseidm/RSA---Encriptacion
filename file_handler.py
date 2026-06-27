
from tkinter import filedialog


def exportar_claves_txt(n, e, d, escribir_resultado, mostrar_aviso):
    ruta = filedialog.asksaveasfilename(
        title="Guardar claves RSA",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")])
    if not ruta:
        escribir_resultado("⚠ Exportación cancelada.")
        return False
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f"n={n}\n")
            f.write(f"e={e}\n")
            f.write(f"d={d}\n")
        escribir_resultado("── Claves exportadas ────────────────────────")
        escribir_resultado(f"  Ruta: {ruta}")
        escribir_resultado("")
        mostrar_aviso("✔ Claves guardadas correctamente.")
        return True
    except Exception:
        escribir_resultado("⚠ Error al exportar claves")
        return False


def importar_claves_txt(escribir_resultado):
    ruta = filedialog.askopenfilename(
        title="Importar claves RSA",
        initialdir="~/Desktop",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not ruta:
        escribir_resultado("⚠ Importación cancelada.")
        return None
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.read().splitlines()
        datos = {}
        for linea in lineas:
            if "=" in linea:
                clave, valor = linea.split("=", 1)
                datos[clave.strip()] = int(valor.strip())
        if "n" not in datos or "d" not in datos:
            escribir_resultado("⚠ El archivo no contiene claves válidas (n, d).")
            return None
        escribir_resultado("── Claves importadas ────────────────────────")
        escribir_resultado(f"  n = {datos['n']}  |  d = {datos['d']}")
        escribir_resultado("")
        return datos
    except Exception:
        escribir_resultado("⚠ Error al importar claves")
        return None


def abrir_archivo_txt(widget_texto, escribir_resultado):
    ruta = filedialog.askopenfilename(
        title="Selecciona un archivo",
        initialdir="~/Desktop",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not ruta:
        return
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        widget_texto.delete("1.0", "end")
        widget_texto.insert("end", contenido.strip())
        escribir_resultado(f"── Archivo cargado: {ruta}")
    except Exception as ex:
        escribir_resultado(f"⚠ Error: {ex}")


def guardar_mensaje_txt(mensaje, titulo, escribir_resultado):
    if mensaje is None:
        escribir_resultado("⚠ No hay mensaje para guardar.")
        return
    ruta = filedialog.asksaveasfilename(
        title=titulo,
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")])
    if not ruta:
        escribir_resultado("⚠ Guardado cancelado.")
        return
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(mensaje)
        escribir_resultado("── Mensaje guardado ─────────────────────────")
        escribir_resultado(f"  Ruta: {ruta}")
        escribir_resultado("")
    except Exception:
        escribir_resultado("⚠ Error al guardar")
