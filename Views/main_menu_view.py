import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME

PALETTE = THEME

class MainMenuView_1(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master

        master.title("Facturación y Pagos")
        master.geometry("550x380")
        master.resizable(False, False)
        master.configure(bg=PALETTE["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"])
        style.configure("Menu.TButton",
                       font=("Segoe UI", 12),
                       padding=15,
                       foreground=PALETTE["text"],
                       background=PALETTE["white"],
                       borderwidth=1,
                       relief="flat")
        style.map("Menu.TButton",
                 background=[("active", PALETTE["secondary"])],
                 foreground=[("active", "white")])

        self.pack(expand=True, fill="both")

        # Header
        header = tk.Frame(self, bg=PALETTE["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Facturación y Pagos", bg=PALETTE["primary"],
                fg="white", font=("Segoe UI", 20, "bold")).pack(pady=20)

        # Container
        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=40, pady=30)

        ttk.Label(container, text="Seleccione un módulo", background=PALETTE["bg"],
                 foreground=PALETTE["text"], font=("Segoe UI", 12)).pack(pady=(0, 20))

        btn_fact = ttk.Button(container, text="Facturación", style="Menu.TButton",
                             command=self._open_facturacion, cursor="hand2")
        btn_fact.pack(pady=8, fill="x", ipady=5)

        btn_pagos = ttk.Button(container, text="Pagos", style="Menu.TButton",
                              command=self._open_pagos, cursor="hand2")
        btn_pagos.pack(pady=8, fill="x", ipady=5)

        btn_volver = ttk.Button(container, text="← Volver al Menú Principal",
                               style="Menu.TButton", command=self._go_back, cursor="hand2")
        btn_volver.pack(pady=20, fill="x", ipady=5)

    def _open_facturacion(self):
        self.controller.open_facturacion_module()

    def _open_pagos(self):
        self.controller.open_pagos_module()

    def _go_back(self):
        self.controller.go_back_to_main_menu()

    def _close(self):
        self.master.quit()
