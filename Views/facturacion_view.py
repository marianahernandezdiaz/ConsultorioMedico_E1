import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME

from Models.factura_model import FacturaModel

PALETTE = THEME

class FacturacionView(ttk.Frame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.model = FacturaModel()
        self.items = []

        master.title("Facturación")
        master.geometry("850x600")
        master.configure(bg=PALETTE["bg"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"])
        style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=("Segoe UI", 10))
        style.configure("Form.TEntry", fieldbackground=PALETTE["white"], font=("Segoe UI", 10))
        style.configure("Primary.TButton", padding=10, foreground="white", background=PALETTE["primary"], font=("Segoe UI", 10))
        style.map("Primary.TButton", background=[("active", PALETTE["secondary"])])
        style.configure("Treeview", background=PALETTE["white"], fieldbackground=PALETTE["white"], font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", background=PALETTE["primary"], foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", PALETTE["primary"])], foreground=[("selected", "white")])

        self.pack(expand=True, fill="both")

        # Header
        header = tk.Frame(self, bg=PALETTE["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Facturación", bg=PALETTE["primary"], fg="white",
                font=("Segoe UI", 20, "bold")).pack(pady=20)

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(top, text="ID Paciente:").grid(row=0, column=0, sticky="w")
        self.paciente_entry = ttk.Entry(top, width=15, style="Form.TEntry")
        self.paciente_entry.grid(row=0, column=1, padx=5)

        ttk.Label(top, text="ID Cita:").grid(row=0, column=2, sticky="w")
        self.cita_entry = ttk.Entry(top, width=15, style="Form.TEntry")
        self.cita_entry.grid(row=0, column=3, padx=5)

        ttk.Label(top, text="Fecha:").grid(row=0, column=4, sticky="w")
        self.fecha_entry = ttk.Entry(top, width=12, style="Form.TEntry")
        self.fecha_entry.grid(row=0, column=5, padx=5)
        self.fecha_entry.insert(0, date.today().isoformat())

        mid = ttk.Frame(self)
        mid.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Servicio", "Cantidad", "Precio")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10)

        ttk.Label(form, text="Servicio").grid(row=0, column=0)
        self.serv_entry = ttk.Entry(form, width=25, style="Form.TEntry")
        self.serv_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Cantidad").grid(row=0, column=2)
        self.cant_entry = ttk.Entry(form, width=8, style="Form.TEntry")
        self.cant_entry.grid(row=0, column=3, padx=5)
        self.cant_entry.insert(0, "1")

        ttk.Label(form, text="Precio").grid(row=0, column=4)
        self.precio_entry = ttk.Entry(form, width=10, style="Form.TEntry")
        self.precio_entry.grid(row=0, column=5, padx=5)

        ttk.Button(form, text="Agregar", style="Primary.TButton", command=self.add_item).grid(row=0, column=6, padx=10)
        ttk.Button(form, text="Eliminar", style="Primary.TButton", command=self.del_item).grid(row=0, column=7)

        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=10)

        self.total_var = tk.StringVar(value="0.00")
        ttk.Label(bottom, text="Total:").pack(side="left")
        ttk.Label(bottom, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(side="left", padx=10)

        # Botón Volver
        if self.controller:
            ttk.Button(bottom, text="← Volver", style="Primary.TButton", command=self.controller.open_facturacion_menu).pack(side="right", padx=5)

        ttk.Button(bottom, text="Guardar Factura", style="Primary.TButton", command=self.save_factura).pack(side="right")

    def add_item(self):
        s = self.serv_entry.get().strip()
        try:
            c = int(self.cant_entry.get().strip())
            p = float(self.precio_entry.get().strip())
        except Exception:
            messagebox.showerror("Error", "Cantidad y Precio deben ser válidos", parent=self)
            return
        if not s:
            messagebox.showerror("Error", "Servicio requerido", parent=self)
            return
        self.items.append((s, c, p))
        self.tree.insert("", "end", values=(s, c, f"{p:.2f}"))
        self.update_total()

    def del_item(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        self.tree.delete(sel[0])
        del self.items[idx]
        self.update_total()

    def update_total(self):
        total = sum(c * p for _, c, p in self.items)
        self.total_var.set(f"{total:.2f}")

    def save_factura(self):
        pid_text = self.paciente_entry.get().strip()
        id_pac = None
        if pid_text:
            try:
                id_pac = int(pid_text)
            except Exception:
                messagebox.showerror("Error", "ID Paciente inválido", parent=self)
                return
            if not self.model.paciente_exists(id_pac):
                messagebox.showerror("Error", "Paciente no existe", parent=self)
                return
        else:
            id_pac = self.model.create_demo_paciente()
            if not id_pac:
                messagebox.showerror("Error", "No se pudo crear paciente de prueba", parent=self)
                return
        id_cita_txt = self.cita_entry.get().strip()
        id_cita = int(id_cita_txt) if id_cita_txt else None
        if id_cita is not None and not self.model.cita_exists(id_cita):
            messagebox.showerror("Error", "La Cita indicada no existe", parent=self)
            return
        fecha = self.fecha_entry.get().strip()
        total = float(self.total_var.get())

        fid = self.model.create_factura(id_cita, id_pac, fecha, total, "Pendiente")
        if not fid:
            messagebox.showerror("Error", "No se pudo crear la factura", parent=self)
            return

        for (nombre, c, p) in self.items:
            sid = self.model.get_or_create_servicio(nombre, p)
            if not sid:
                messagebox.showerror("Error", "No se pudo registrar servicio", parent=self)
                return
            self.model.add_detalle(fid, sid, c, p)

        messagebox.showinfo("OK", f"Factura {fid} creada", parent=self)
        self.items.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.update_total()

    def destroy(self):
        self.model.close()
        super().destroy()
