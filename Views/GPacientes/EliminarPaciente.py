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


def abrir_ventana_eliminar_paciente(master, controller):
    """
    Ventana para BUSCAR un paciente por ID y ELIMINARLO.
    """

    win = tk.Toplevel(master)
    win.title("Eliminar Paciente")
    win.geometry("600x350")
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
        text="Eliminar paciente",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ---------- Contenido ----------
    frame_main = tk.Frame(win, bg=PALETA["frame"], padx=15, pady=15)
    frame_main.pack(fill="both", expand=True, padx=20, pady=(15, 5))

    frame_main.columnconfigure(0, weight=0)
    frame_main.columnconfigure(1, weight=1)

    # --- Buscar por ID ---
    tk.Label(
        frame_main,
        text="ID Paciente:",
        bg=PALETA["frame"],
        anchor="w"
    ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

    entry_id = tk.Entry(frame_main, width=10)
    entry_id.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    # Área para mostrar información del paciente
    info_label = tk.Label(
        frame_main,
        text="Datos del paciente:",
        bg=PALETA["frame"],
        anchor="w",
        font=("Arial", 10, "bold")
    )
    info_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(15, 5), padx=5)

    text_info = tk.Text(frame_main, width=50, height=6, state="disabled")
    text_info.grid(row=2, column=0, columnspan=3, pady=5, padx=5)

    def mostrar_info(texto):
        text_info.config(state="normal")
        text_info.delete("1.0", tk.END)
        text_info.insert(tk.END, texto)
        text_info.config(state="disabled")

    def limpiar_info():
        mostrar_info("")

    def cargar_paciente():
        id_txt = entry_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un ID numérico de paciente.")
            limpiar_info()
            return

        paciente = controller.obtener_paciente_por_id(int(id_txt))
        if not paciente:
            messagebox.showinfo("No encontrado", "No se encontró un paciente con ese ID.")
            limpiar_info()
            return

        # Construimos un resumen de los datos
        resumen = (
            f"ID: {paciente['ID_Paciente']}\n"
            f"Nombre: {paciente['Nombres']} {paciente['Apellidos']}\n"
            f"Fecha nac.: {paciente['Fecha_nac']}\n"
            f"Teléfono: {paciente.get('Telefono') or ''}\n"
            f"Dirección: {paciente.get('Direccion') or ''}\n"
            f"Seguro médico: {paciente.get('Seguro_Med') or ''}\n"
        )
        mostrar_info(resumen)

    ttk.Button(
        frame_main,
        text="Buscar",
        style="Secondary.TButton",
        command=cargar_paciente
    ).grid(row=0, column=2, padx=10, pady=5)

    # ---------- Botones inferior ----------
    frame_botones = tk.Frame(win, bg=PALETA["fondo"])
    frame_botones.pack(side="bottom", pady=10)

    def eliminar_paciente():
        id_txt = entry_id.get().strip()
        if not id_txt.isdigit():
            messagebox.showwarning("ID inválido", "Ingresa un ID numérico válido.")
            return

        # Confirmación
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar a este paciente?\n"
            "Esta acción no se puede deshacer."
        )
        if not confirmar:
            return

        try:
            ok = controller.eliminar_paciente(int(id_txt))
            if ok:
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
                win.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "No se pudo eliminar el paciente. Verifica el ID."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar:\n{e}")

    ttk.Button(
        frame_botones,
        text="Eliminar",
        style="Primary.TButton",
        command=eliminar_paciente
    ).grid(row=0, column=0, padx=10, pady=5)

    ttk.Button(
        frame_botones,
        text="Cancelar",
        style="Secondary.TButton",
        command=win.destroy
    ).grid(row=0, column=1, padx=10, pady=5)
