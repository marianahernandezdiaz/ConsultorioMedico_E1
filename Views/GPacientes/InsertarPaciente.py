import tkinter as tk
from tkinter import ttk, messagebox

# Paleta de colores
PALETA = {
    "header": "#247D7F",       # Barra superior / títulos
    "fondo": "#B2D9C4",        # Fondo de la ventana
    "frame": "#80B9C8",        # Fondo del formulario
    "btn_principal": "#247D7F",
    "btn_secundario": "#44916F",
    "accent": "#C29470"
}


def abrir_ventana_insertar_paciente(master, controller):

    win = tk.Toplevel(master)
    win.title("Insertar Paciente")
    win.geometry("650x450")
    win.config(bg=PALETA["fondo"])
    win.grab_set()  # para que tenga el foco hasta cerrar

    # --------- Estilos ttk para botones ----------
    style = ttk.Style(win)
    style.theme_use("clam")

    style.configure(
        "Primary.TButton",
        background=PALETA["btn_principal"],
        foreground="white",
        padding=6
    )
    style.map(
        "Primary.TButton",
        background=[("active", PALETA["accent"])]
    )

    style.configure(
        "Secondary.TButton",
        background=PALETA["btn_secundario"],
        foreground="white",
        padding=6
    )
    style.map(
        "Secondary.TButton",
        background=[("active", PALETA["header"])]
    )

    # --------- Helper para crear filas de etiqueta + entry ----------
    def add_labeled_entry(parent, label_text, row, width=30):
        tk.Label(
            parent,
            text=label_text,
            bg=PALETA["frame"],
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=5, padx=5)

        entry = tk.Entry(parent, width=width)
        entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        return entry

    # --------- Header ----------
    header = tk.Frame(win, bg=PALETA["header"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Registro de nuevo paciente",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # --------- Formulario ----------
    frame_form = tk.Frame(win, bg=PALETA["frame"], padx=15, pady=15, bd=0)
    frame_form.pack(fill="both", expand=True, padx=20, pady=(15, 5))

    frame_form.columnconfigure(0, weight=0)
    frame_form.columnconfigure(1, weight=1)

    # Campos que SÍ existen en la tabla Pacientes
    entry_nombres = add_labeled_entry(frame_form, "Nombres:", 0)
    entry_apellidos = add_labeled_entry(frame_form, "Apellidos:", 1)

    # Fecha de nacimiento (texto simple con formato YYYY-MM-DD)
    tk.Label(
        frame_form,
        text="Fecha de nacimiento (YYYY-MM-DD):",
        bg=PALETA["frame"],
        anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=5, padx=5)

    entry_fecha_nac = tk.Entry(frame_form, width=20)
    entry_fecha_nac.grid(row=2, column=1, sticky="w", pady=5, padx=5)

    entry_telefono = add_labeled_entry(frame_form, "Teléfono:", 3)
    entry_direccion = add_labeled_entry(frame_form, "Dirección:", 4, width=40)
    entry_seguro = add_labeled_entry(frame_form, "Seguro médico:", 5)

    # --------- Guardar ----------
    def guardar_paciente():
        nombres = entry_nombres.get().strip()
        apellidos = entry_apellidos.get().strip()
        fecha_nac = entry_fecha_nac.get().strip()

        if not nombres or not apellidos or not fecha_nac:
            messagebox.showwarning(
                "Campos obligatorios",
                "Nombres, Apellidos y Fecha de nacimiento son obligatorios."
            )
            return

        datos = {
            "nombres": nombres,
            "apellidos": apellidos,
            "fecha_nac": fecha_nac,  # formato 'YYYY-MM-DD'
            "telefono": entry_telefono.get().strip(),
            "direccion": entry_direccion.get().strip(),
            "seguro_med": entry_seguro.get().strip(),
        }

        try:
            controller.insertar_paciente(datos)
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar:\n{e}")

    # --------- Botones ---------
    frame_botones = tk.Frame(win, bg=PALETA["fondo"])
    frame_botones.pack(side="bottom", pady=10)

    ttk.Button(
        frame_botones,
        text="Guardar",
        style="Primary.TButton",
        command=guardar_paciente
    ).grid(row=0, column=0, padx=10, pady=5)

    ttk.Button(
        frame_botones,
        text="Cancelar",
        style="Secondary.TButton",
        command=win.destroy
    ).grid(row=0, column=1, padx=10, pady=5)
