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
from tema_config import THEME

PALETA = THEME


class PacientesMenuPrincipalView(tk.Frame):
    def __init__(self, root_principal, main_controller=None):
        super().__init__(root_principal)
        self.root_principal = root_principal
        self.main_controller = main_controller
        self.controller = PacienteController()

        root_principal.title("Gestión de Pacientes")
        root_principal.geometry("800x550")
        root_principal.config(bg=PALETA["bg"])

        self.config(bg=PALETA["bg"])
        self.pack(expand=True, fill="both")

        self._create_widgets()

    def _create_widgets(self):
        # Estilos ttk (¡nombres únicos para este módulo!)
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "PacientesPrimary.TButton",
            background=PALETA["white"],
            foreground=PALETA["text"],
            padding=15,
            font=("Segoe UI", 11),
            borderwidth=1,
            relief="flat"
        )
        style.map(
            "PacientesPrimary.TButton",
            background=[("active", PALETA["secondary"])],
            foreground=[("active", "white")]
        )

        style.configure(
            "PacientesSecondary.TButton",
            background=PALETA["accent"],
            foreground="white",
            padding=10,
            font=("Segoe UI", 10)
        )
        style.map(
            "PacientesSecondary.TButton",
            background=[("active", PALETA["secondary"])]
        )

        # Encabezado
        header = tk.Frame(self, bg=PALETA["primary"])
        header.pack(fill="x")

        tk.Label(
            header,
            text="Gestión de Pacientes",
            bg=PALETA["primary"],
            fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self, bg=PALETA["bg"])
        main_container.pack(expand=True, fill="both", padx=40, pady=30)

        tk.Label(
            main_container,
            text="Seleccione una operación",
            bg=PALETA["bg"],
            fg=PALETA["text"],
            font=("Segoe UI", 12)
        ).pack(pady=(0, 20))

        # Frame de botones central
        frame_botones = tk.Frame(main_container, bg=PALETA["bg"], padx=20, pady=20)
        frame_botones.pack(expand=True, fill="both")

        # Botones CRUD
        ttk.Button(
            frame_botones,
            text="Insertar",
            style="PacientesPrimary.TButton",
            command=lambda: abrir_ventana_insertar_paciente(self.root_principal, self.controller)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(
            frame_botones,
            text="Buscar",
            style="PacientesPrimary.TButton",
            command=lambda: abrir_ventana_buscar_paciente(self.root_principal, self.controller)
        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Button(
            frame_botones,
            text="Modificar",
            style="PacientesPrimary.TButton",
            command=lambda: abrir_ventana_modificar_paciente(self.root_principal, self.controller)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(
            frame_botones,
            text="Eliminar",
            style="PacientesPrimary.TButton",
            command=lambda: abrir_ventana_eliminar_paciente(self.root_principal, self.controller)
        ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Button(
            frame_botones,
            text="Listar",
            style="PacientesPrimary.TButton",
            command=lambda: abrir_ventana_listar_pacientes(self.root_principal, self.controller)
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=(15, 5), sticky="ew")

        for i in range(2):
            frame_botones.columnconfigure(i, weight=1)

        # Botón Volver al Menú Principal
        if self.main_controller:
            frame_volver = tk.Frame(self, bg=PALETA["bg"])
            frame_volver.pack(side="bottom", pady=20)

            ttk.Button(
                frame_volver,
                text="← Volver al Menú Principal",
                style="PacientesSecondary.TButton",
                command=self.main_controller.go_back_to_main_menu,
                cursor="hand2"
            ).pack()


def PacientesMenuPrincipal(root_principal=None, main_controller=None):
    """
    Función wrapper para mantener compatibilidad con código existente.
    Si se llama desde otro módulo, crea un Frame.
    Si se ejecuta solo, crea su propio Tk.
    """
    if root_principal is None:
        root = tk.Tk()
        view = PacientesMenuPrincipalView(root, main_controller)
        root.mainloop()
    else:
        return PacientesMenuPrincipalView(root_principal, main_controller)


if __name__ == "__main__":
    PacientesMenuPrincipal()
