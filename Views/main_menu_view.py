import tkinter as tk
from tkinter import ttk

PALETTE = {
    "primary": "#247D7F",
    "secondary": "#44916F",
    "accent": "#B2D9C4",
    "bg": "#80B9C8",
    "warn": "#C29470",
}

class MainMenuView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title("Menú Principal")
        self.geometry("500x300")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"]) 
        style.configure("TLabel", background=PALETTE["bg"], foreground="#0F3D3E")
        style.configure(
            "Menu.TButton",
            font=("Arial", 12, "bold"),
            padding=10,
            foreground="white",
            background=PALETTE["primary"],
        )
        style.map("Menu.TButton", background=[("active", PALETTE["secondary"])])
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", background=PALETTE["accent"], foreground="#0F3D3E", font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", PALETTE["primary"])], foreground=[("selected", "white")])

        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        title_lbl = ttk.Label(container, text="Sistema de Consultorio", font=("Arial", 16, "bold"))
        title_lbl.pack(pady=10)

        btn_fact = ttk.Button(container, text="Facturación", style="Menu.TButton", command=self._open_facturacion)
        btn_fact.pack(pady=10, fill="x")

        btn_pagos = ttk.Button(container, text="Pagos", style="Menu.TButton", command=self._open_pagos)
        btn_pagos.pack(pady=10, fill="x")

        btn_salir = ttk.Button(container, text="Salir", command=self._close)
        btn_salir.pack(pady=20)

        self.transient(master)
        self.grab_set()

    def _open_facturacion(self):
        self.controller.open_facturacion_module()

    def _open_pagos(self):
        self.controller.open_pagos_module()

    def _close(self):
        self.grab_release()
        self.destroy()
