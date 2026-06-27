# main.py — Interfaz gráfica principal (Tkinter) — Criptografía RSA
# Importa la lógica desde rsa_logic.py y el manejo de archivos desde file_handler.py

import tkinter as tk
from tkinter import scrolledtext

import rsa_logic as rsa
import file_handler as fh

# ── ESTADO GLOBAL ────────────────────────────────────────────
n_global      = None
euler_global  = None
d_global      = None
e_global      = None
dec_resultado = None

ventana_proceso = None
txt_proceso     = None
proceso_logs    = []

# ── TEMAS ────────────────────────────────────────────────────
TEMAS = {
    "claro": {
        "BG":     "white",
        "NEGRO":  "#111827",
        "GRIS":   "#6b7280",
        "BORDE":  "#e5e7eb",
        "ENTRY":  "white",
        "FG_ENT": "#111827",
    },
    "oscuro": {
        "BG":     "#0d1117",
        "NEGRO":  "#e6edf3",
        "GRIS":   "#8b949e",
        "BORDE":  "#30363d",
        "ENTRY":  "#161b22",
        "FG_ENT": "#e6edf3",
    }
}

tema_actual = "claro"

AZUL  = "#2563eb"
VERDE = "#16a34a"
ROJO  = "#dc2626"

def T(key):
    return TEMAS[tema_actual][key]

# ── CONSOLA ──────────────────────────────────────────────────

def escribir_resultado(texto):
    proceso_logs.append(texto)
    if txt_proceso is not None and ventana_proceso is not None and ventana_proceso.winfo_exists():
        txt_proceso.configure(state="normal")
        txt_proceso.insert(tk.END, texto + "\n")
        txt_proceso.configure(state="disabled")
        txt_proceso.see(tk.END)

def limpiar_resultado():
    proceso_logs.clear()
    if txt_proceso is not None and ventana_proceso is not None and ventana_proceso.winfo_exists():
        txt_proceso.configure(state="normal")
        txt_proceso.delete("1.0", tk.END)
        txt_proceso.configure(state="disabled")

# ── SECCIONES ────────────────────────────────────────────────

def mostrar_seccion(frame):
    frame.pack(fill="x", pady=0)

def ocultar_seccion(frame):
    frame.pack_forget()

def ocultar_enc_desde_sec2():
    for f in [enc_sec2_frame, enc_sec3_frame, enc_sec4_frame, enc_sec5_frame]:
        ocultar_seccion(f)

def ocultar_enc_desde_sec3():
    for f in [enc_sec3_frame, enc_sec4_frame, enc_sec5_frame]:
        ocultar_seccion(f)

# ── LÓGICA ENCRIPTAR ─────────────────────────────────────────

def calcular_n_euler():
    global n_global, euler_global

    limpiar_resultado()
    ocultar_enc_desde_sec2()

    p = enc_campo_p.get()
    if not p.isdigit():
        enc_estado_p.config(text="✘ no es número", fg=ROJO)
        return
    p = int(p)
    if not rsa.es_primo(p):
        enc_estado_p.config(text="✘ no es primo", fg=ROJO)
        return
    enc_estado_p.config(text="✔ primo", fg=VERDE)

    q = enc_campo_q.get()
    if not q.isdigit():
        enc_estado_q.config(text="✘ no es número", fg=ROJO)
        return
    q = int(q)
    if not rsa.es_primo(q):
        enc_estado_q.config(text="✘ no es primo", fg=ROJO)
        return
    enc_estado_q.config(text="✔ primo", fg=VERDE)

    n_global     = p * q
    euler_global = rsa.calcular_euler(p, q)

    if n_global <= 255:
        enc_estado_p.config(text="✘ primo pequeño", fg=ROJO)
        enc_estado_q.config(text="✘ primo pequeño", fg=ROJO)
        enc_label_advertencia.config(
            text="Primos muy pequeños, ingresa primos a partir de p=17, q=19.")
        escribir_resultado("ATENCION: Números primos muy pequeños.")
        escribir_resultado(f"  n = {p} × {q} = {n_global}")
        escribir_resultado("n debe ser mayor que 255 (ASCII 0-255).")
        n_global = None
        euler_global = None
        return

    if p == q:
        enc_estado_p.config(text="✘ igual a q", fg=ROJO)
        enc_estado_q.config(text="✘ igual a p", fg=ROJO)
        enc_label_advertencia.config(text="Primos iguales, ingresa primos diferentes.")
        escribir_resultado("ATENCION: P y Q, segun RSA no pueden ser iguales.")
        return

    enc_estado_p.config(text="✔ primo", fg=VERDE)
    enc_estado_q.config(text="✔ primo", fg=VERDE)
    enc_label_advertencia.config(text="")

    escribir_resultado("── PASO 1 — Números primos ──────────────────")
    escribir_resultado(f"  p = {p}  |  q = {q}")
    escribir_resultado("")
    escribir_resultado("── PASO 2 — Calcular n y φ(n) ───────────────")
    escribir_resultado(f"  n    = {p} × {q} = {n_global}")
    escribir_resultado(f"  φ(n) = ({p}-1) × ({q}-1) = {euler_global}")
    escribir_resultado("")

    mostrar_seccion(enc_sec2_frame)
    mostrar_candidatos_d()


def mostrar_candidatos_d():
    for widget in enc_frame_d.winfo_children():
        widget.destroy()

    candidatos = rsa.obtener_candidatos_d(euler_global)

    escribir_resultado("── PASO 3 — Candidatos de d ─────────────────")
    escribir_resultado(f"  Valores válidos: {candidatos}")
    escribir_resultado("")

    for valor in candidatos:
        rb = tk.Radiobutton(
            enc_frame_d, text=str(valor), variable=enc_d_valor, value=str(valor),
            font=F_MONO, bg=T("BG"), fg=T("NEGRO"),
            activebackground=T("BG"), selectcolor=T("BG"))
        rb.pack(side="left", padx=2)

    enc_d_valor.set(str(candidatos[0]))


def confirmar_d():
    global d_global, e_global

    ocultar_enc_desde_sec3()

    d_global = int(enc_d_valor.get())
    e_global = rsa.calcular_e(d_global, euler_global)

    escribir_resultado("── PASO 4 — Calcular e ──────────────────────")
    escribir_resultado(f"  d elegido = {d_global}")
    escribir_resultado(f"  e × {d_global} ≡ 1 mod {euler_global}  →  e = {e_global}")
    escribir_resultado("")
    escribir_resultado("── RESULTADO — Claves generadas ─────────────")
    escribir_resultado(f"  Clave pública  (n, e) = ({n_global}, {e_global})")
    escribir_resultado(f"  Clave privada  (n, d) = ({n_global}, {d_global})")
    escribir_resultado("")

    enc_etiqueta_clave_publica.config(text=f"Clave pública:   (n={n_global},  e={e_global})")
    enc_etiqueta_clave_privada.config(text=f"Clave privada:   (n={n_global},  d={d_global})")
    enc_label_exportar_aviso.config(text="⚠ Guarda las claves antes de continuar.")

    mostrar_seccion(enc_sec3_frame)


def encriptar_mensaje():
    mensaje = enc_txt_mensaje.get("1.0", tk.END).strip()
    if not mensaje:
        escribir_resultado("IMPORTANTE: No hay mensaje para encriptar.")
        return None
    try:
        mensaje_final = rsa.encriptar(mensaje, e_global, n_global)
        escribir_resultado("── PASO 5 — Encriptar mensaje (RSA) ─────────")
        escribir_resultado(f"  Clave pública usada: (n={n_global}, e={e_global})")
        escribir_resultado(f"  Mensaje original:    {mensaje}")
        escribir_resultado(f"  Fórmula aplicada:    c = m^e mod n")
        escribir_resultado(f"  Mensaje encriptado:  {mensaje_final}")
        escribir_resultado("")
        return mensaje_final
    except Exception:
        escribir_resultado("⚠ Error al encriptar")
        return None


def guardar_mensaje_enc():
    mensaje = encriptar_mensaje()
    fh.guardar_mensaje_txt(mensaje, "Guardar mensaje encriptado", escribir_resultado)


def exportar_claves():
    fh.exportar_claves_txt(
        n_global, e_global, d_global,
        escribir_resultado,
        lambda txt: enc_label_exportar_aviso.config(text=txt)
    )
    mostrar_seccion(enc_sec4_frame)
    mostrar_seccion(enc_sec5_frame)


def abrir_archivo_enc():
    fh.abrir_archivo_txt(enc_txt_mensaje, escribir_resultado)

# ── LÓGICA DESENCRIPTAR ──────────────────────────────────────

def importar_claves():
    global n_global, d_global, e_global
    datos = fh.importar_claves_txt(escribir_resultado)
    if datos:
        n_global = datos["n"]
        d_global = datos["d"]
        e_global = datos.get("e", None)
        dec_etiqueta_claves.config(text=f"Claves cargadas:   n={n_global}   d={d_global}")
        mostrar_seccion(dec_sec2)


def abrir_archivo_dec():
    fh.abrir_archivo_txt(dec_txt_mensaje, escribir_resultado)


def desencriptar_mensaje():
    global dec_resultado
    mensaje = dec_txt_mensaje.get("1.0", tk.END).strip()
    if not mensaje:
        escribir_resultado("⚠ No hay mensaje para desencriptar.")
        return
    try:
        mensaje_original = rsa.desencriptar(mensaje, d_global, n_global)
        dec_resultado = mensaje_original
        dec_txt_resultado.configure(state="normal")
        dec_txt_resultado.delete("1.0", tk.END)
        dec_txt_resultado.insert(tk.END, mensaje_original)
        dec_txt_resultado.configure(state="disabled")
        escribir_resultado("── Desencriptar mensaje (RSA) ───────────────")
        escribir_resultado(f"  Clave privada usada: (n={n_global}, d={d_global})")
        escribir_resultado(f"  Fórmula aplicada:    m = c^d mod n")
        escribir_resultado(f"  Mensaje original:    {mensaje_original}")
        escribir_resultado("")
    except Exception:
        escribir_resultado("⚠ Error al desencriptar")


def guardar_mensaje_dec():
    fh.guardar_mensaje_txt(dec_resultado, "Guardar mensaje desencriptado", escribir_resultado)

# ── CAMBIO DE MODO ───────────────────────────────────────────

def mostrar_modo_encriptar():
    ocultar_seccion(dec_frame)
    mostrar_seccion(enc_frame)

def mostrar_modo_desencriptar():
    ocultar_seccion(enc_frame)
    mostrar_seccion(dec_frame)

# ── CAMBIO DE TEMA ───────────────────────────────────────────

todos_los_widgets = []

def registrar_widget(w, tipo="frame"):
    todos_los_widgets.append((w, tipo))
    return w

def aplicar_tema():
    bg    = T("BG")
    fg    = T("NEGRO")
    gris  = T("GRIS")
    borde = T("BORDE")
    entry = T("ENTRY")
    fg_e  = T("FG_ENT")

    root.configure(bg=bg)
    main_canvas.configure(bg=bg)
    barra_inferior.configure(bg=bg)

    for widget, tipo in todos_los_widgets:
        try:
            if tipo == "frame":
                widget.configure(bg=bg)
            elif tipo == "label":
                widget.configure(bg=bg, fg=fg)
            elif tipo == "label_gris":
                widget.configure(bg=bg, fg=gris)
            elif tipo == "label_verde":
                widget.configure(bg=bg, fg=VERDE)
            elif tipo == "label_rojo":
                widget.configure(bg=bg, fg=ROJO)
            elif tipo == "sep":
                widget.configure(bg=borde)
            elif tipo == "entry":
                widget.configure(bg=entry, fg=fg_e, insertbackground=fg_e)
            elif tipo == "text":
                widget.configure(bg=entry, fg=fg_e, insertbackground=fg_e)
            elif tipo == "canvas":
                widget.configure(bg=bg)
        except Exception:
            pass

    btn_tema.configure(
        text="☀️ Modo claro" if tema_actual == "oscuro" else "🌙 Modo oscuro",
        bg=bg, fg=fg, activebackground=bg, activeforeground=fg
    )

def toggle_tema():
    global tema_actual
    tema_actual = "oscuro" if tema_actual == "claro" else "claro"
    aplicar_tema()

# ============================================================
#   INTERFAZ
# ============================================================

root = tk.Tk()
root.title("Criptografía RSA")
root.geometry("600x820")
root.configure(bg="white")
root.resizable(True, True)

F      = ("Arial", 10)
F_B    = ("Arial", 10, "bold")
F_T    = ("Arial", 13, "bold")
F_MONO = ("Courier New", 10)

# ── SCROLL PRINCIPAL ─────────────────────────────────────────
main_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
scrollbar   = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
main_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

scroll_frame  = tk.Frame(main_canvas, bg="white")
scroll_window = main_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
registrar_widget(scroll_frame, "frame")

def on_frame_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))
scroll_frame.bind("<Configure>", on_frame_configure)

def on_canvas_configure(event):
    main_canvas.itemconfig(scroll_window, width=event.width)
main_canvas.bind("<Configure>", on_canvas_configure)

def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
main_canvas.bind_all("<MouseWheel>", _on_mousewheel)


def hacer_seccion_frame(parent, titulo):
    contenedor = tk.Frame(parent, bg=T("BG"))
    registrar_widget(contenedor, "frame")
    lbl = tk.Label(contenedor, text=titulo, font=F_T, bg=T("BG"), fg=T("NEGRO"))
    lbl.pack(anchor="w", padx=24, pady=(18, 4))
    registrar_widget(lbl, "label")
    sep = tk.Frame(contenedor, bg=T("BORDE"), height=1)
    sep.pack(fill="x", padx=24)
    registrar_widget(sep, "sep")
    return contenedor

def boton(parent, texto, color, comando=None, lado=None):
    b = tk.Button(parent, text=texto, bg=color, fg="white",
                  font=F_B, relief="flat", cursor="hand2",
                  padx=16, pady=7, bd=0,
                  activebackground=color, activeforeground="white",
                  command=comando)
    if lado:
        b.pack(side=lado, padx=(0, 10))
    else:
        b.pack(anchor="w", padx=24, pady=6)
    return b

# ── SELECTOR DE MODO ─────────────────────────────────────────
modo_frame = tk.Frame(scroll_frame, bg="white")
modo_frame.pack(fill="x", pady=0)
registrar_widget(modo_frame, "frame")

lbl_titulo = tk.Label(modo_frame, text="Criptografía RSA", font=("Arial", 16, "bold"),
                      bg="white", fg="#111827")
lbl_titulo.pack(anchor="w", padx=24, pady=(20, 4))
registrar_widget(lbl_titulo, "label")

sep_modo = tk.Frame(modo_frame, bg="#e5e7eb", height=1)
sep_modo.pack(fill="x", padx=24)
registrar_widget(sep_modo, "sep")

lbl_que = tk.Label(modo_frame, text="¿Qué deseas hacer?", font=F_B,
                   bg="white", fg="#6b7280")
lbl_que.pack(anchor="w", padx=24, pady=(10, 4))
registrar_widget(lbl_que, "label_gris")

fila_modo = tk.Frame(modo_frame, bg="white")
fila_modo.pack(anchor="w", padx=24, pady=(0, 14))
registrar_widget(fila_modo, "frame")
boton(fila_modo, " Encriptar",    AZUL, comando=mostrar_modo_encriptar,    lado="left")
boton(fila_modo, " Desencriptar", "#6b7280", comando=mostrar_modo_desencriptar, lado="left")

# ── MODO ENCRIPTAR ───────────────────────────────────────────
enc_frame = tk.Frame(scroll_frame, bg="white")
registrar_widget(enc_frame, "frame")

enc_sec1 = hacer_seccion_frame(enc_frame, "1. Números primos")
enc_sec1.pack(fill="x")

fila1 = tk.Frame(enc_sec1, bg="white")
fila1.pack(anchor="w", padx=24, pady=8)
registrar_widget(fila1, "frame")

lbl_p = tk.Label(fila1, text="p =", font=F_B, bg="white", fg="#111827")
lbl_p.pack(side="left")
registrar_widget(lbl_p, "label")
enc_campo_p = tk.Entry(fila1, width=6, font=F_MONO, relief="solid", bd=1)
enc_campo_p.pack(side="left", padx=(6, 4))
registrar_widget(enc_campo_p, "entry")
enc_estado_p = tk.Label(fila1, text="", font=("Arial", 9), bg="white", width=12)
enc_estado_p.pack(side="left")
registrar_widget(enc_estado_p, "label")

lbl_q = tk.Label(fila1, text="q =", font=F_B, bg="white", fg="#111827")
lbl_q.pack(side="left", padx=(20, 0))
registrar_widget(lbl_q, "label")
enc_campo_q = tk.Entry(fila1, width=6, font=F_MONO, relief="solid", bd=1)
enc_campo_q.pack(side="left", padx=(6, 4))
registrar_widget(enc_campo_q, "entry")
enc_estado_q = tk.Label(fila1, text="", font=("Arial", 9), bg="white", width=12)
enc_estado_q.pack(side="left")
registrar_widget(enc_estado_q, "label")

tk.Button(fila1, text="Calcular n y φ(n)", bg=AZUL, fg="white", font=F_B,
          relief="flat", cursor="hand2", padx=16, pady=7, bd=0,
          activebackground=AZUL, activeforeground="white",
          command=calcular_n_euler).pack(side="left", padx=(20, 0))

enc_label_advertencia = tk.Label(enc_sec1, text="", font=("Arial", 9), bg="white", fg=ROJO)
enc_label_advertencia.pack(anchor="w", padx=24)
registrar_widget(enc_label_advertencia, "frame")

enc_sec2_frame = hacer_seccion_frame(enc_frame, "2. Seleccionar d")

enc_canvas_d = tk.Canvas(enc_sec2_frame, bg="white", height=35, highlightthickness=0)
registrar_widget(enc_canvas_d, "canvas")
enc_scroll_d = tk.Scrollbar(enc_sec2_frame, orient="horizontal", command=enc_canvas_d.xview)
enc_canvas_d.configure(xscrollcommand=enc_scroll_d.set)
enc_canvas_d.pack(fill="x", padx=24)
enc_scroll_d.pack(fill="x", padx=24)

enc_frame_d = tk.Frame(enc_canvas_d, bg="white")
registrar_widget(enc_frame_d, "frame")
enc_canvas_d.create_window((0, 0), window=enc_frame_d, anchor="nw")

def enc_actualizar_scroll(event):
    enc_canvas_d.configure(scrollregion=enc_canvas_d.bbox("all"))
enc_frame_d.bind("<Configure>", enc_actualizar_scroll)

enc_d_valor = tk.StringVar()
boton(enc_sec2_frame, "Confirmar d y calcular e", AZUL, comando=confirmar_d)

enc_sec3_frame = hacer_seccion_frame(enc_frame, "3. Claves generadas")

enc_etiqueta_clave_publica = tk.Label(enc_sec3_frame, text="Clave pública:   —", font=F_MONO, bg="white", fg=VERDE)
enc_etiqueta_clave_publica.pack(anchor="w", padx=24, pady=2)
registrar_widget(enc_etiqueta_clave_publica, "label_verde")

enc_etiqueta_clave_privada = tk.Label(enc_sec3_frame, text="Clave privada:   —", font=F_MONO, bg="white", fg=ROJO)
enc_etiqueta_clave_privada.pack(anchor="w", padx=24, pady=(2, 4))
registrar_widget(enc_etiqueta_clave_privada, "label_rojo")

fila_exportar = tk.Frame(enc_sec3_frame, bg="white")
fila_exportar.pack(anchor="w", padx=24, pady=(0, 4))
registrar_widget(fila_exportar, "frame")
boton(fila_exportar, " Exportar claves (.txt)", VERDE, comando=exportar_claves, lado="left")

enc_label_exportar_aviso = tk.Label(enc_sec3_frame, text="", font=("Arial", 9), bg="white", fg=ROJO)
enc_label_exportar_aviso.pack(anchor="w", padx=24, pady=(0, 10))
registrar_widget(enc_label_exportar_aviso, "frame")

enc_sec4_frame = hacer_seccion_frame(enc_frame, "4. Encriptar mensaje")

lbl_enc_msg = tk.Label(enc_sec4_frame, text="Escribe o carga el mensaje a encriptar:",
                       font=F, bg="white", fg="#6b7280")
lbl_enc_msg.pack(anchor="w", padx=24, pady=(8, 2))
registrar_widget(lbl_enc_msg, "label_gris")

enc_txt_mensaje = tk.Text(enc_sec4_frame, height=3, font=F_MONO, relief="solid", bd=1,
                          padx=8, pady=6, bg="white", fg="#111827")
enc_txt_mensaje.pack(fill="x", padx=24, pady=(0, 4))
registrar_widget(enc_txt_mensaje, "text")

fila_enc_botones = tk.Frame(enc_sec4_frame, bg="white")
fila_enc_botones.pack(anchor="w", padx=24, pady=(0, 10))
registrar_widget(fila_enc_botones, "frame")
boton(fila_enc_botones, "Abrir archivo .txt",   VERDE, lado="left", comando=abrir_archivo_enc)
boton(fila_enc_botones, "Encriptar",            AZUL,  lado="left", comando=encriptar_mensaje)
boton(fila_enc_botones, "Guardar mensaje .txt", VERDE, lado="left", comando=guardar_mensaje_enc)

enc_sec5_frame = enc_sec4_frame

# ── MODO DESENCRIPTAR ────────────────────────────────────────
dec_frame = tk.Frame(scroll_frame, bg="white")
registrar_widget(dec_frame, "frame")

dec_sec1 = hacer_seccion_frame(dec_frame, "1. Importar claves RSA")
dec_sec1.pack(fill="x")

lbl_dec_clave = tk.Label(dec_sec1, text="Carga el archivo .txt con las claves (n, d):",
                         font=F, bg="white", fg="#6b7280")
lbl_dec_clave.pack(anchor="w", padx=24, pady=(8, 2))
registrar_widget(lbl_dec_clave, "label_gris")

dec_etiqueta_claves = tk.Label(dec_sec1, text="Claves cargadas:   —", font=F_MONO, bg="white", fg=VERDE)
dec_etiqueta_claves.pack(anchor="w", padx=24, pady=(0, 4))
registrar_widget(dec_etiqueta_claves, "label_verde")

boton(dec_sec1, " Importar claves (.txt)", AZUL, comando=importar_claves)

sep_dec = tk.Frame(dec_frame, bg="#e5e7eb", height=1)
sep_dec.pack(fill="x", padx=24, pady=4)
registrar_widget(sep_dec, "sep")

dec_sec2 = hacer_seccion_frame(dec_frame, "2. Desencriptar mensaje")

lbl_dec_msg = tk.Label(dec_sec2, text="Pega o carga el mensaje encriptado (Base64):",
                       font=F, bg="white", fg="#6b7280")
lbl_dec_msg.pack(anchor="w", padx=24, pady=(8, 2))
registrar_widget(lbl_dec_msg, "label_gris")

dec_txt_mensaje = tk.Text(dec_sec2, height=3, font=F_MONO, relief="solid", bd=1,
                          padx=8, pady=6, bg="white", fg="#111827")
dec_txt_mensaje.pack(fill="x", padx=24, pady=(0, 4))
registrar_widget(dec_txt_mensaje, "text")

fila_dec_botones = tk.Frame(dec_sec2, bg="white")
fila_dec_botones.pack(anchor="w", padx=24, pady=(0, 10))
registrar_widget(fila_dec_botones, "frame")
boton(fila_dec_botones, "Abrir archivo .txt",   VERDE, lado="left", comando=abrir_archivo_dec)
boton(fila_dec_botones, "Desencriptar",         AZUL,  lado="left", comando=desencriptar_mensaje)
boton(fila_dec_botones, "Guardar mensaje .txt", VERDE, lado="left", comando=guardar_mensaje_dec)

lbl_dec_res = tk.Label(dec_sec2, text="Mensaje desencriptado:", font=F, bg="white", fg="#6b7280")
lbl_dec_res.pack(anchor="w", padx=24, pady=(0, 4))
registrar_widget(lbl_dec_res, "label_gris")

dec_txt_resultado = tk.Text(dec_sec2, height=3, font=F_MONO, relief="solid", bd=1,
                            padx=8, pady=6, bg="white", fg="#111827", state="disabled")
dec_txt_resultado.pack(fill="x", padx=24, pady=(0, 14))
registrar_widget(dec_txt_resultado, "text")

# ── BARRA INFERIOR ───────────────────────────────────────────

def abrir_ventana_proceso():
    global ventana_proceso, txt_proceso
    if ventana_proceso is not None and ventana_proceso.winfo_exists():
        ventana_proceso.lift()
        return
    ventana_proceso = tk.Toplevel(root)
    ventana_proceso.title("Proceso / Resultados")
    ventana_proceso.geometry("620x420")
    ventana_proceso.configure(bg=T("BG"))
    ventana_proceso.resizable(True, True)
    tk.Label(ventana_proceso, text="Proceso y Resultados",
             font=F_T, bg=T("BG"), fg=T("NEGRO")).pack(anchor="w", padx=24, pady=(18, 4))
    txt_proceso = scrolledtext.ScrolledText(
        ventana_proceso, height=18, font=F_MONO, relief="solid", bd=1,
        bg=T("ENTRY"), fg=T("NEGRO"), padx=8, pady=8, state="disabled", wrap="word")
    txt_proceso.pack(fill="both", expand=True, padx=24, pady=(0, 10))
    if proceso_logs:
        txt_proceso.configure(state="normal")
        txt_proceso.insert(tk.END, "\n".join(proceso_logs) + "\n")
        txt_proceso.configure(state="disabled")
    else:
        txt_proceso.configure(state="normal")
        txt_proceso.insert(tk.END, "Aquí aparecerán los resultados del proceso.")
        txt_proceso.configure(state="disabled")

    def cerrar_ventana():
        global ventana_proceso, txt_proceso
        ventana_proceso.destroy()
        ventana_proceso = None
        txt_proceso = None

    ventana_proceso.protocol("WM_DELETE_WINDOW", cerrar_ventana)
    fila_botones = tk.Frame(ventana_proceso, bg=T("BG"))
    fila_botones.pack(anchor="w", padx=24, pady=6)
    boton(fila_botones, "Cerrar",  "#6b7280", comando=cerrar_ventana,    lado="left")
    boton(fila_botones, "Limpiar", "#6b7280", comando=limpiar_resultado, lado="left")


barra_inferior = tk.Frame(root, bg="white")
barra_inferior.pack(side="bottom", fill="x")
registrar_widget(barra_inferior, "frame")

sep_barra = tk.Frame(barra_inferior, bg="#e5e7eb", height=1)
sep_barra.pack(fill="x", pady=(6, 0))
registrar_widget(sep_barra, "sep")

fila_ver = tk.Frame(barra_inferior, bg="white")
fila_ver.pack(side="left", padx=24, pady=6)
registrar_widget(fila_ver, "frame")

tk.Button(fila_ver, text="Ver proceso", bg=AZUL, fg="white",
          font=F_B, relief="flat", cursor="hand2",
          padx=16, pady=7, bd=0,
          activebackground=AZUL, activeforeground="white",
          command=abrir_ventana_proceso).pack(side="left", padx=(0, 10))

lbl_proceso = tk.Label(fila_ver, text="Resultados / Proceso", font=F_T,
                       bg="white", fg="#111827")
lbl_proceso.pack(side="left")
registrar_widget(lbl_proceso, "label")

# Botón de tema
btn_tema = tk.Button(barra_inferior, text="🌙 Modo oscuro",
                     bg="white", fg="#111827", font=F_B,
                     relief="flat", cursor="hand2", padx=16, pady=7, bd=0,
                     activebackground="white", activeforeground="#111827",
                     command=toggle_tema)
btn_tema.pack(side="right", padx=24, pady=6)

mostrar_modo_encriptar()
root.mainloop()