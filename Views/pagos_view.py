import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME

from Models.factura_model import FacturaModel

PALETTE = THEME

class PagosView(ttk.Frame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.model = FacturaModel()

        master.title("Pagos")
        master.geometry("850x550")
        master.configure(bg=PALETTE["bg"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=("Segoe UI", 10))
        style.configure("Primary.TButton", padding=10, foreground="white", background=PALETTE["primary"], font=("Segoe UI", 10))
        style.map("Primary.TButton", background=[("active", PALETTE["secondary"])])
        style.configure("Treeview", background=PALETTE["white"], fieldbackground=PALETTE["white"], font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", background=PALETTE["primary"], foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", PALETTE["primary"])], foreground=[("selected", "white")])

        self.pack(expand=True, fill="both")

        # Header
        header = tk.Frame(self, bg=PALETTE["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Gestión de Pagos", bg=PALETTE["primary"], fg="white",
                font=("Segoe UI", 20, "bold")).pack(pady=20)

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)
        ttk.Button(top, text="Ver Pendientes", style="Primary.TButton", command=self.load_pendientes).pack(side="left", padx=5)
        ttk.Button(top, text="Ver Todas", style="Primary.TButton", command=self.load_todas).pack(side="left", padx=5)
        ttk.Button(top, text="Marcar Pagado", style="Primary.TButton", command=self.mark_pagado).pack(side="right", padx=5)

        # Botón Volver
        if self.controller:
            ttk.Button(top, text="← Volver", style="Primary.TButton", command=self.controller.open_facturacion_menu).pack(side="right", padx=5)

        cols = ("ID", "Paciente", "Total", "Estado")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_pendientes()

    def load_todas(self):
        rows = self.model.list_facturas()
        self._load(rows)

    def load_pendientes(self):
        rows = self.model.list_facturas("Pendiente")
        self._load(rows)

    def _load(self, rows):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert("", "end", values=(r['ID_Factura'], r['ID_Paciente'], f"{r['Total']:.2f}", r['Estado_Pago']))

    def mark_pagado(self):
        sel = self.tree.selection()
        if not sel:
            return
        fid = int(self.tree.item(sel[0], "values")[0])
        ok = self.model.set_estado(fid, "Pagado")
        if ok:
            messagebox.showinfo("OK", f"Factura {fid} marcada como Pagado", parent=self)
            self.load_pendientes()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado", parent=self)

    def destroy(self):
        self.model.close()
        super().destroy()
