import tkinter as tk
from tkinter import ttk

import os
import sys

# Agrega la carpeta raíz del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Controllers.PacientesController import PacienteController
from Views.GPacientes.InsertarPaciente import abrir_ventana_insertar_paciente
from Views.GPacientes.BuscarPaciente import abrir_ventana_buscar_paciente
from Views.GPacientes.ModificarPaciente import abrir_ventana_modificar_paciente
from Views.GPacientes.EliminarPaciente import abrir_ventana_eliminar_paciente
from Views.GPacientes.ListarPaciente import abrir_ventana_listar_pacientes

PALETA = {
    "header": "#247D7F",       # Barra superior / títulos
    "fondo": "#B2D9C4",        # Fondo de la ventana
    "frame": "#80B9C8",        # Fondo de contenedores
    "btn_principal": "#247D7F",
    "btn_secundario": "#44916F",
    "accent": "#C29470"
}


def PacientesMenuPrincipal(root_principal=None):
    """
    Muestra la ventana principal del módulo de Gestión de Pacientes.
    Si se llama desde otro módulo, pásale su root como root_principal.
    Si se ejecuta solo, crea su propio root.
    """
    controller = PacienteController()

    if root_principal is None:
        root = tk.Tk()
    else:
        root = tk.Toplevel(root_principal)

    root.title("Gestión de Pacientes")
    root.geometry("700x450")
    root.config(bg=PALETA["fondo"])

    # Estilos ttk
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("Primary.TButton", background=PALETA["btn_principal"], foreground="white", padding=8, font=("Arial", 11, "bold") )
    style.map("Primary.TButton", background=[("active", PALETA["accent"])]
    )

    # Encabezado
    header = tk.Frame(root, bg=PALETA["header"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Módulo de Gestión de Pacientes",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    tk.Label(
        root,
        text="Elige la accion deseas realizar:",
        bg=PALETA["fondo"],
        fg="#1e4e5a",
        font=("Arial", 13)
    ).pack(pady=10)

    # Frame de botones central
    frame_botones = tk.Frame(root, bg=PALETA["frame"], padx=20, pady=20)
    frame_botones.pack(pady=20, padx=40, fill="x")

    # Botones CRUD
    ttk.Button(
        frame_botones,
        text="Insertar",
        style="Primary.TButton",
        command=lambda: abrir_ventana_insertar_paciente(root, controller)
    ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Buscar",
        style="Primary.TButton",
        command=lambda: abrir_ventana_buscar_paciente(root, controller)
    ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Modificar",
        style="Primary.TButton",
        command=lambda: abrir_ventana_modificar_paciente(root, controller)
    ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Eliminar",
        style="Primary.TButton",
        command=lambda: abrir_ventana_eliminar_paciente(root, controller)
    ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Listar",
        style="Primary.TButton",
        command=lambda: abrir_ventana_listar_pacientes(root, controller)
    ).grid(row=2, column=0, columnspan=2, padx=10, pady=(15, 5), sticky="ew")

    for i in range(2):
        frame_botones.columnconfigure(i, weight=1)

    if root_principal is None:  # Si se ejecuta como módulo independiente
        root.mainloop()


if __name__ == "__main__":
    PacientesMenuPrincipal()


