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
# from Views.GPacientes.BuscarPaciente import abrir_ventana_buscar_paciente
from Views.GPacientes.ModificarPaciente import abrir_ventana_modificar_paciente
from Views.GPacientes.EliminarPaciente import abrir_ventana_eliminar_paciente
# from Views.GPacientes.ListarPaciente import abrir_ventana_listar_pacientes


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
    root.config(bg="#e3f2fd")

    style = ttk.Style()
    style.theme_use("clam")

    # Encabezado
    header = tk.Frame(root, bg="#42a5f5")
    header.pack(fill="x")

    tk.Label(
        header,
        text="Módulo de Gestión de Pacientes",
        bg="#42a5f5",
        fg="white",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    tk.Label(
        root,
        text="Sistema de gestión de pacientes",
        bg="#e3f2fd",
        fg="#1e88e5",
        font=("Arial", 12)
    ).pack(pady=10)

    frame_botones = tk.Frame(root, bg="#e3f2fd")
    frame_botones.pack(pady=20)

    # Botones CRUD (por ahora sin comando)
    ttk.Button(
        frame_botones,
        text="Insertar",
        # command=lambda: print("Insertar paciente (GUI)")
        command=lambda: abrir_ventana_insertar_paciente(root, controller )
    ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Buscar",
        command=lambda: print("Buscar paciente (WIP)")
    ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Modificar",
        # command=lambda: print("Modificar paciente (WIP)")
        command=lambda: abrir_ventana_modificar_paciente(root, controller)
    ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Eliminar",
        # command=lambda: print("Eliminar paciente (WIP)")
        command=lambda: abrir_ventana_eliminar_paciente(root, controller)
    ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    ttk.Button(
        frame_botones,
        text="Listar",
        command=lambda: print("Listar pacientes (WIP)")
    ).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    for i in range(2):
        frame_botones.columnconfigure(i, weight=1)

    if root_principal is None:  # Si se ejecuta como módulo independiente
        root.mainloop()


# ESTA PARTE FALTABA
if __name__ == "__main__":
    PacientesMenuPrincipal()
