import tkinter as tk
from tkinter import ttk, messagebox

# Misma paleta que las demás vistas
PALETA = {
    "header": "#247D7F",
    "fondo": "#B2D9C4",
    "frame": "#80B9C8",
    "btn_principal": "#247D7F",
    "btn_secundario": "#44916F",
    "accent": "#C29470"
}


def abrir_ventana_modificar_paciente(master, controller):
    """
    Ventana para BUSCAR un paciente por ID y MODIFICAR sus datos.
    """

    win = tk.Toplevel(master)
    win.title("Modificar Paciente")
    win.geometry("650x500")
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
        text="Modificar datos de paciente",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ---------- Formulario ----------
    frame_form = tk.Frame(win, bg=PALETA["frame"], padx=15, pady=15)
    frame_form.pack(fill="both", expand=True, padx=20, pady=(15, 5))

    frame_form.columnconfigure(0, weight=0)
    frame_form.columnconfigure(1, weight=1)

    # --- Fila 0: Buscar por ID ---
    tk.Label(
        frame_form,
        text="ID Paciente:",
        bg=PALETA["frame"],
        anchor="w"
    ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

    entry_id = tk.Entry(frame_form, width=10)
    entry_id.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    def cargar_paciente():
        id_txt = entry_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un ID numérico de paciente.")
            return

        paciente = controller.obtener_paciente_por_id(int(id_txt))
        if not paciente:
            messagebox.showinfo("No encontrado", "No se encontró un paciente con ese ID.")
            limpiar_campos()
            return

        # Llenar campos
        entry_nombres.delete(0, tk.END)
        entry_nombres.insert(0, paciente["Nombres"])

        entry_apellidos.delete(0, tk.END)
        entry_apellidos.insert(0, paciente["Apellidos"])

        entry_fecha_nac.delete(0, tk.END)
        entry_fecha_nac.insert(0, str(paciente["Fecha_nac"]))

        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, paciente.get("Telefono") or "")

        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, paciente.get("Direccion") or "")

        entry_seguro.delete(0, tk.END)
        entry_seguro.insert(0, paciente.get("Seguro_Med") or "")

    ttk.Button(
        frame_form,
        text="Cargar",
        style="Secondary.TButton",
        command=cargar_paciente
    ).grid(row=0, column=2, padx=10, pady=5)

    # Helper para entradas
    def add_labeled_entry(label, row, width=30):
        tk.Label(
            frame_form,
            text=label,
            bg=PALETA["frame"],
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=5, padx=5)

        e = tk.Entry(frame_form, width=width)
        e.grid(row=row, column=1, columnspan=2, sticky="w", pady=5, padx=5)
        return e

    # Campos editables (igual que la tabla Pacientes)
    entry_nombres = add_labeled_entry("Nombres:", 1)
    entry_apellidos = add_labeled_entry("Apellidos:", 2)

    tk.Label(
        frame_form,
        text="Fecha de nacimiento (YYYY-MM-DD):",
        bg=PALETA["frame"],
        anchor="w"
    ).grid(row=3, column=0, sticky="w", pady=5, padx=5)
    entry_fecha_nac = tk.Entry(frame_form, width=20)
    entry_fecha_nac.grid(row=3, column=1, sticky="w", pady=5, padx=5)

    entry_telefono = add_labeled_entry("Teléfono:", 4)
    entry_direccion = add_labeled_entry("Dirección:", 5)
    entry_seguro = add_labeled_entry("Seguro médico:", 6)

    def limpiar_campos():
        entry_nombres.delete(0, tk.END)
        entry_apellidos.delete(0, tk.END)
        entry_fecha_nac.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_seguro.delete(0, tk.END)

    # --- Guardar cambios ---
    def guardar_cambios():
        id_txt = entry_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un ID numérico válido.")
            return

        if not entry_nombres.get().strip() or not entry_apellidos.get().strip() or not entry_fecha_nac.get().strip():
            messagebox.showwarning(
                "Campos obligatorios",
                "Nombres, Apellidos y Fecha de nacimiento son obligatorios."
            )
            return

        datos = {
            "nombres": entry_nombres.get().strip(),
            "apellidos": entry_apellidos.get().strip(),
            "fecha_nac": entry_fecha_nac.get().strip(),
            "telefono": entry_telefono.get().strip(),
            "direccion": entry_direccion.get().strip(),
            "seguro_med": entry_seguro.get().strip(),
        }

        try:
            actualizado = controller.actualizar_paciente(int(id_txt), datos)
            if actualizado:
                messagebox.showinfo("Éxito", "Datos del paciente actualizados correctamente.")
                win.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el paciente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar:\n{e}")

    # ---------- Botones inferior ----------
    frame_botones = tk.Frame(win, bg=PALETA["fondo"])
    frame_botones.pack(side="bottom", pady=10)

    ttk.Button(
        frame_botones,
        text="Guardar cambios",
        style="Primary.TButton",
        command=guardar_cambios
    ).grid(row=0, column=0, padx=10, pady=5)

    ttk.Button(
        frame_botones,
        text="Cancelar",
        style="Secondary.TButton",
        command=win.destroy
    ).grid(row=0, column=1, padx=10, pady=5)
