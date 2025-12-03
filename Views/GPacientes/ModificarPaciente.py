import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

# Usar el mismo tema global que el resto del sistema
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME


def abrir_ventana_modificar_paciente(master, controller):
    """
    Ventana para BUSCAR un paciente por ID y MODIFICAR sus datos.
    """

    win = tk.Toplevel(master)
    win.title("Modificar Paciente")
    win.geometry("700x520")
    win.config(bg=THEME["bg"])
    win.grab_set()

    # ---------- Estilos ----------
    style = ttk.Style(win)
    style.theme_use("clam")

    # Botones
    style.configure(
        "Primary.TButton",
        background=THEME["success"],
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

    # Entradas
    style.configure(
        "TEntry",
        fieldbackground=THEME["white"],
        foreground=THEME["text"],
        borderwidth=1
    )

    # ---------- Header ----------
    header = tk.Frame(win, bg=THEME["primary"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Modificar datos de paciente",
        bg=THEME["primary"],
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=10)

    # ---------- Contenedor principal ----------
    contenedor = tk.Frame(win, bg=THEME["bg"])
    contenedor.pack(fill="both", expand=True, padx=20, pady=(15, 10))

    # ---------- Formulario ----------
    frame_form = tk.Frame(
        contenedor,
        bg=THEME["white"],
        padx=20,
        pady=20,
        bd=1,
        relief=tk.SOLID
    )
    frame_form.pack(fill="both", expand=True)

    frame_form.columnconfigure(0, weight=0)
    frame_form.columnconfigure(1, weight=1)
    frame_form.columnconfigure(2, weight=0)

    # --- Fila 0: Buscar por ID ---
    tk.Label(
        frame_form,
        text="ID Paciente:",
        bg=THEME["white"],
        fg=THEME["text"],
        anchor="w",
        font=("Segoe UI", 10, "bold")
    ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

    entry_id = ttk.Entry(frame_form, width=10)
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
    ).grid(row=0, column=2, padx=10, pady=5, sticky="e")

    # Helper para entradas
    def add_labeled_entry(label, row, width=35):
        tk.Label(
            frame_form,
            text=label,
            bg=THEME["white"],
            fg=THEME["text"],
            anchor="w",
            font=("Segoe UI", 10, "bold")
        ).grid(row=row, column=0, sticky="w", pady=5, padx=5)

        e = ttk.Entry(frame_form, width=width)
        e.grid(row=row, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
        return e

    # Campos editables (igual que la tabla Pacientes)
    entry_nombres = add_labeled_entry("Nombres:", 1)
    entry_apellidos = add_labeled_entry("Apellidos:", 2)

    tk.Label(
        frame_form,
        text="Fecha de nacimiento (YYYY-MM-DD):",
        bg=THEME["white"],
        fg=THEME["text"],
        anchor="w",
        font=("Segoe UI", 10, "bold")
    ).grid(row=3, column=0, sticky="w", pady=5, padx=5)

    entry_fecha_nac = ttk.Entry(frame_form, width=20)
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
    frame_botones = tk.Frame(contenedor, bg=THEME["bg"])
    frame_botones.pack(fill="x", pady=10)

    frame_botones.columnconfigure(0, weight=1)
    frame_botones.columnconfigure(1, weight=0)
    frame_botones.columnconfigure(2, weight=0)

    ttk.Button(
        frame_botones,
        text="Guardar cambios",
        style="Primary.TButton",
        command=guardar_cambios
    ).grid(row=0, column=1, padx=10, pady=5, sticky="e")

    ttk.Button(
        frame_botones,
        text="Cancelar",
        style="Secondary.TButton",
        command=win.destroy
    ).grid(row=0, column=2, padx=10, pady=5, sticky="e")
