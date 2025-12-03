import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

# Usar el mismo tema global
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME


def abrir_ventana_buscar_paciente(master, controller):
    """
    Ventana para buscar un paciente por ID y mostrar sus datos (solo lectura).
    """

    win = tk.Toplevel(master)
    win.title("Buscar Paciente")
    win.geometry("650x450")
    win.config(bg=THEME["bg"])
    win.grab_set()

    # ---------- Estilos ----------
    style = ttk.Style(win)
    style.theme_use("clam")

    style.configure(
        "Primary.TButton",
        background=THEME["primary"],
        foreground="white",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )
    style.map(
        "Primary.TButton",
        background=[("active", THEME["accent"])]
    )

    style.configure(
        "Secondary.TButton",
        background=THEME["secondary"],
        foreground="white",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )
    style.map(
        "Secondary.TButton",
        background=[("active", THEME["primary"])]
    )

    # ---------- Header ----------
    header = tk.Frame(win, bg=THEME["primary"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Buscar paciente por ID",
        bg=THEME["primary"],
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=10)

    # ---------- Contenedor principal ----------
    contenedor = tk.Frame(win, bg=THEME["bg"])
    contenedor.pack(fill="both", expand=True, padx=20, pady=(10, 10))

    # ---------- Zona de búsqueda ----------
    frame_search = tk.Frame(contenedor, bg=THEME["white"], padx=15, pady=10, bd=1, relief=tk.SOLID)
    frame_search.pack(fill="x")

    frame_search.columnconfigure(0, weight=0)
    frame_search.columnconfigure(1, weight=1)
    frame_search.columnconfigure(2, weight=0)

    tk.Label(
        frame_search,
        text="ID Paciente:",
        bg=THEME["white"],
        fg=THEME["text"],
        anchor="w",
        font=("Segoe UI", 10, "bold")
    ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

    entry_id = ttk.Entry(frame_search, width=10)
    entry_id.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    # ---------- Zona de datos (solo lectura) ----------
    frame_datos = tk.Frame(contenedor, bg=THEME["white"], padx=15, pady=15, bd=1, relief=tk.SOLID)
    frame_datos.pack(fill="both", expand=True, pady=(10, 0))

    frame_datos.columnconfigure(0, weight=0)
    frame_datos.columnconfigure(1, weight=1)

    def add_row(label_text, row):
        tk.Label(
            frame_datos,
            text=label_text,
            bg=THEME["white"],
            fg=THEME["text"],
            anchor="w",
            font=("Segoe UI", 10, "bold")
        ).grid(row=row, column=0, sticky="w", pady=3, padx=5)

        lbl_val = tk.Label(
            frame_datos,
            text="-",
            bg=THEME["white"],
            fg=THEME["text"],
            anchor="w",
            font=("Segoe UI", 10)
        )
        lbl_val.grid(row=row, column=1, sticky="w", pady=3, padx=5)
        return lbl_val

    lbl_val_id = add_row("ID:", 0)
    lbl_val_nombres = add_row("Nombres:", 1)
    lbl_val_apellidos = add_row("Apellidos:", 2)
    lbl_val_fecha = add_row("Fecha de nacimiento:", 3)
    lbl_val_tel = add_row("Teléfono:", 4)
    lbl_val_dir = add_row("Dirección:", 5)
    lbl_val_seg = add_row("Seguro médico:", 6)

    def limpiar_datos():
        lbl_val_id.config(text="-")
        lbl_val_nombres.config(text="-")
        lbl_val_apellidos.config(text="-")
        lbl_val_fecha.config(text="-")
        lbl_val_tel.config(text="-")
        lbl_val_dir.config(text="-")
        lbl_val_seg.config(text="-")

    def buscar_paciente():
        id_txt = entry_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un ID numérico de paciente.")
            limpiar_datos()
            return

        try:
            paciente = controller.obtener_paciente_por_id(int(id_txt))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al buscar:\n{e}")
            limpiar_datos()
            return

        if not paciente:
            messagebox.showinfo("No encontrado", "No se encontró un paciente con ese ID.")
            limpiar_datos()
            return

        # Mostrar datos (solo lectura)
        lbl_val_id.config(text=str(paciente["ID_Paciente"]))
        lbl_val_nombres.config(text=paciente["Nombres"])
        lbl_val_apellidos.config(text=paciente["Apellidos"])
        lbl_val_fecha.config(text=str(paciente["Fecha_nac"]))
        lbl_val_tel.config(text=paciente.get("Telefono") or "")
        lbl_val_dir.config(text=paciente.get("Direccion") or "")
        lbl_val_seg.config(text=paciente.get("Seguro_Med") or "")

    ttk.Button(
        frame_search,
        text="Buscar",
        style="Secondary.TButton",
        command=buscar_paciente
    ).grid(row=0, column=2, padx=10, pady=5, sticky="e")

    # ---------- Botón cerrar ----------
    frame_botones = tk.Frame(contenedor, bg=THEME["bg"])
    frame_botones.pack(fill="x", pady=10)

    frame_botones.columnconfigure(0, weight=1)
    frame_botones.columnconfigure(1, weight=0)

    ttk.Button(
        frame_botones,
        text="Cerrar",
        style="Primary.TButton",
        command=win.destroy
    ).grid(row=0, column=1, padx=10, pady=5, sticky="e")
