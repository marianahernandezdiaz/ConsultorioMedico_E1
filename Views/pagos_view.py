import tkinter as tk
from tkinter import ttk, messagebox

from Controllers.pagos_controller import PagosController

PALETTE = {
    "primary": "#247D7F",
    "secondary": "#44916F",
    "accent": "#B2D9C4",
    "bg": "#80B9C8",
    "warn": "#C29470",
}

class PagosView(tk.Toplevel):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller or PagosController()

        self.title("Pagos")
        self.geometry("700x450")
        self.configure(bg=PALETTE["bg"]) 
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"]) 
        style.configure("TLabel", background=PALETTE["bg"], foreground="#0F3D3E")
        style.configure("Primary.TButton", padding=8, foreground="white", background=PALETTE["primary"]) 
        style.map("Primary.TButton", background=[["active", PALETTE["secondary"]]])
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", background=PALETTE["accent"], foreground="#0F3D3E", font=("Arial", 11, "bold"))
        style.map("Treeview", background=[["selected", PALETTE["primary"]]], foreground=[["selected", "white"]])

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)
        ttk.Button(top, text="Ver Pendientes", style="Primary.TButton", command=self.load_pendientes).pack(side="left", padx=5)
        ttk.Button(top, text="Ver Todas", style="Primary.TButton", command=self.load_todas).pack(side="left", padx=5)
        ttk.Button(top, text="Marcar Pagado", style="Primary.TButton", command=self.mark_pagado).pack(side="right")

        cols = ("ID", "Paciente", "Total", "Estado")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_pendientes()

        self.transient(master)
        self.grab_set()

    def load_todas(self):
        rows = self.controller.list_facturas()
        self._load(rows)

    def load_pendientes(self):
        rows = self.controller.list_facturas("Pendiente")
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
        ok = self.controller.set_estado(fid, "Pagado")
        if ok:
            messagebox.showinfo("OK", f"Factura {fid} marcada como Pagado", parent=self)
            self.load_pendientes()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado", parent=self)

    def destroy(self):
        self.controller.close()
        self.grab_release()
        super().destroy()
