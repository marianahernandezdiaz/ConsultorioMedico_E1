import tkinter as tk
from tkinter import ttk, messagebox

PALETA = {
    "header": "#247D7F",
    "fondo": "#B2D9C4",
    "frame": "#80B9C8",
    "btn_principal": "#247D7F",
    "btn_secundario": "#44916F",
    "accent": "#C29470"
}


def abrir_ventana_buscar_paciente(master, controller):
    """
    Ventana para buscar un paciente por ID y mostrar sus datos (solo lectura).
    """

    win = tk.Toplevel(master)
    win.title("Buscar Paciente")
    win.geometry("650x400")
    win.config(bg=PALETA["fondo"])
    win.grab_set()

    # ---------- Estilos ----------
    style = ttk.Style(win)
    style.theme_use("clam")

    style.configure(
        "Primary.TButton",
        background=PALETA["btn_principal"],
        foreground="white",
        padding=6
    )
    style.map("Primary.TButton", background=[("active", PALETA["accent"])])

    style.configure(
        "Secondary.TButton",
        background=PALETA["btn_secundario"],
        foreground="white",
        padding=6
    )
    style.map("Secondary.TButton", background=[("active", PALETA["header"])])

    # ---------- Header ----------
    header = tk.Frame(win, bg=PALETA["header"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Buscar paciente por ID",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ---------- Zona de búsqueda ----------
    frame_search = tk.Frame(win, bg=PALETA["frame"], padx=15, pady=10)
    frame_search.pack(fill="x", padx=20, pady=(10, 5))

    tk.Label(
        frame_search,
        text="ID Paciente:",
        bg=PALETA["frame"],
        anchor="w"
    ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

    entry_id = tk.Entry(frame_search, width=10)
    entry_id.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    # ---------- Zona de datos (solo lectura) ----------
    frame_datos = tk.Frame(win, bg=PALETA["frame"], padx=15, pady=15)
    frame_datos.pack(fill="both", expand=True, padx=20, pady=(5, 10))

    frame_datos.columnconfigure(0, weight=0)
    frame_datos.columnconfigure(1, weight=1)

    def add_row(label_text, row):
        tk.Label(
            frame_datos,
            text=label_text,
            bg=PALETA["frame"],
            anchor="w",
            font=("Arial", 10, "bold")
        ).grid(row=row, column=0, sticky="w", pady=3, padx=5)

        lbl_val = tk.Label(
            frame_datos,
            text="-",
            bg=PALETA["frame"],
            anchor="w"
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
    ).grid(row=0, column=2, padx=10, pady=5)

    # ---------- Botón cerrar ----------
    frame_botones = tk.Frame(win, bg=PALETA["fondo"])
    frame_botones.pack(side="bottom", pady=10)

    ttk.Button(
        frame_botones,
        text="Cerrar",
        style="Primary.TButton",
        command=win.destroy
    ).grid(row=0, column=0, padx=10, pady=5)
