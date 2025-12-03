import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

# Mismo tema global que el resto de vistas
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME


def abrir_ventana_listar_pacientes(master, controller):
    """
    Ventana para listar todos los pacientes en un Treeview.
    """

    win = tk.Toplevel(master)
    win.title("Lista de Pacientes")
    win.geometry("900x565")
    win.config(bg=THEME["bg"])
    win.grab_set()

    # ---------- Estilos ----------
    style = ttk.Style(win)
    style.theme_use("clam")

    # Botones
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

    # Treeview
    style.configure(
        "Treeview.Heading",
        background=THEME["primary"],
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0
    )
    style.configure(
        "Treeview",
        background=THEME["white"],
        fieldbackground=THEME["white"],
        foreground=THEME["text"],
        font=("Segoe UI", 10),
        rowheight=26
    )
    style.map(
        "Treeview",
        background=[("selected", THEME["primary"])],
        foreground=[("selected", "white")]
    )

    # ---------- Header ----------
    header = tk.Frame(win, bg=THEME["primary"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Pacientes registrados",
        bg=THEME["primary"],
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=10)

    # ---------- Contenedor principal ----------
    contenedor = tk.Frame(win, bg=THEME["bg"])
    contenedor.pack(fill="both", expand=True, padx=15, pady=(10, 5))

    frame_main = tk.Frame(contenedor, bg=THEME["white"], padx=10, pady=10, bd=1, relief=tk.SOLID)
    frame_main.pack(fill="both", expand=True)

    # ---------- Treeview ----------
    columns = (
        "ID_Paciente", "Nombres", "Apellidos", "Fecha_nac",
        "Telefono", "Direccion", "Seguro_Med"
    )

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
    tree.column("ID_Paciente", width=50, anchor="center")
    tree.column("Nombres", width=130, anchor="w")
    tree.column("Apellidos", width=130, anchor="w")
    tree.column("Fecha_nac", width=100, anchor="center")
    tree.column("Telefono", width=100, anchor="center")
    tree.column("Direccion", width=200, anchor="w")
    tree.column("Seguro_Med", width=120, anchor="w")

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
    frame_botones = tk.Frame(contenedor, bg=THEME["bg"])
    frame_botones.pack(fill="x", pady=10)

    frame_botones.columnconfigure(0, weight=1)
    frame_botones.columnconfigure(1, weight=0)
    frame_botones.columnconfigure(2, weight=0)

    ttk.Button(
        frame_botones,
        text="Refrescar",
        style="Secondary.TButton",
        command=cargar_datos
    ).grid(row=0, column=1, padx=10, pady=5, sticky="e")

    ttk.Button(
        frame_botones,
        text="Cerrar",
        style="Primary.TButton",
        command=win.destroy
    ).grid(row=0, column=2, padx=10, pady=5, sticky="e")
