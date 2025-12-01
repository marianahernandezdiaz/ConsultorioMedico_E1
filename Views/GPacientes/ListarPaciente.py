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


def abrir_ventana_listar_pacientes(master, controller):
    """
    Ventana para listar todos los pacientes en un Treeview.
    """

    win = tk.Toplevel(master)
    win.title("Lista de Pacientes")
    win.geometry("800x500")
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
        text="Pacientes registrados",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ---------- Frame principal ----------
    frame_main = tk.Frame(win, bg=PALETA["frame"], padx=10, pady=10)
    frame_main.pack(fill="both", expand=True, padx=15, pady=(10, 5))

    # ---------- Treeview ----------
    columns = ("ID_Paciente", "Nombres", "Apellidos", "Fecha_nac",
                "Telefono", "Direccion", "Seguro_Med")

    tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=15)
    tree.pack(side="left", fill="both", expand=True)

    # Encabezados
    tree.heading("ID_Paciente", text="ID")
    tree.heading("Nombres", text="Nombres")
    tree.heading("Apellidos", text="Apellidos")
    tree.heading("Fecha_nac", text="Fecha nac.")
    tree.heading("Telefono", text="Teléfono")
    tree.heading("Direccion", text="Dirección")
    tree.heading("Seguro_Med", text="Seguro médico")

    # Anchos aprox.
    tree.column("ID_Paciente", width=40, anchor="center")
    tree.column("Nombres", width=120)
    tree.column("Apellidos", width=120)
    tree.column("Fecha_nac", width=90, anchor="center")
    tree.column("Telefono", width=90)
    tree.column("Direccion", width=150)
    tree.column("Seguro_Med", width=100)

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(frame_main, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # ---------- Función para cargar datos ----------
    def cargar_datos():
        # Limpiar
        for row in tree.get_children():
            tree.delete(row)

        try:
            pacientes = controller.listar_pacientes()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al obtener los pacientes:\n{e}")
            return

        if not pacientes:
            messagebox.showinfo("Información", "No hay pacientes registrados.")
            return

        # Insertar filas
        for p in pacientes:
            tree.insert(
                "",
                tk.END,
                values=(
                    p["ID_Paciente"],
                    p["Nombres"],
                    p["Apellidos"],
                    str(p["Fecha_nac"]),
                    p.get("Telefono") or "",
                    p.get("Direccion") or "",
                    p.get("Seguro_Med") or "",
                )
            )

    # Cargar al inicio
    cargar_datos()

    # ---------- Botones inferiores ----------
    frame_botones = tk.Frame(win, bg=PALETA["fondo"])
    frame_botones.pack(side="bottom", pady=10)

    ttk.Button(
        frame_botones,
        text="Refrescar",
        style="Secondary.TButton",
        command=cargar_datos
    ).grid(row=0, column=0, padx=10, pady=5)

    ttk.Button(
        frame_botones,
        text="Cerrar",
        style="Primary.TButton",
        command=win.destroy
    ).grid(row=0, column=1, padx=10, pady=5)
