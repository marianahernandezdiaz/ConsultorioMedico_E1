import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from Controllers.facturacion_controller import FacturacionController

PALETTE = {
    "primary": "#247D7F",
    "secondary": "#44916F",
    "accent": "#B2D9C4",
    "bg": "#80B9C8",
    "warn": "#C29470",
}

class FacturacionView(tk.Toplevel):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller or FacturacionController()
        self.items = []

        self.title("Facturación")
        self.geometry("700x500")
        self.configure(bg=PALETTE["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"]) 
        style.configure("TLabel", background=PALETTE["bg"], foreground="#0F3D3E")
        style.configure("Form.TEntry", fieldbackground="#FFFFFF")
        style.configure("Primary.TButton", padding=8, foreground="white", background=PALETTE["primary"]) 
        style.map("Primary.TButton", background=[("active", PALETTE["secondary"])])
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", background=PALETTE["accent"], foreground="#0F3D3E", font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", PALETTE["primary"])], foreground=[("selected", "white")])

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
        ttk.Button(bottom, text="Guardar Factura", style="Primary.TButton", command=self.save_factura).pack(side="right")

        self.transient(master)
        self.grab_set()

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
            if not self.controller.paciente_exists(id_pac):
                messagebox.showerror("Error", "Paciente no existe", parent=self)
                return
        else:
            id_pac = self.controller.create_demo_paciente()
            if not id_pac:
                messagebox.showerror("Error", "No se pudo crear paciente de prueba", parent=self)
                return
        id_cita_txt = self.cita_entry.get().strip()
        id_cita = int(id_cita_txt) if id_cita_txt else None
        if id_cita is not None and not self.controller.cita_exists(id_cita):
            messagebox.showerror("Error", "La Cita indicada no existe", parent=self)
            return
        fecha = self.fecha_entry.get().strip()
        total = float(self.total_var.get())

        fid = self.controller.create_factura(id_cita, id_pac, fecha, total, "Pendiente")
        if not fid:
            messagebox.showerror("Error", "No se pudo crear la factura", parent=self)
            return

        for (nombre, c, p) in self.items:
            sid = self.controller.get_or_create_servicio(nombre, p)
            if not sid:
                messagebox.showerror("Error", "No se pudo registrar servicio", parent=self)
                return
            self.controller.add_detalle(fid, sid, c, p)

        messagebox.showinfo("OK", f"Factura {fid} creada", parent=self)
        self.items.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.update_total()

    def destroy(self):
        self.controller.close()
        self.grab_release()
        super().destroy()
