import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME

class DoctorView(tk.Frame):
    def __init__(self, master, controller, doctor_name):
        super().__init__(master)
        self.controller = controller
        self.master = master

        self.configure(bg=THEME["bg"])
        self.pack(fill=tk.BOTH, expand=True)
        self.master.title(f"Expediente Clínico - Dr. {doctor_name}")
        self.master.geometry("1200x700")
        self.master.config(bg=THEME["bg"])

        self._create_ui()

    def _create_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configurar estilos de Treeview
        style.configure("Treeview.Heading",
                       background=THEME["primary"],
                       foreground="white",
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        style.configure("Treeview",
                       background=THEME["white"],
                       fieldbackground=THEME["white"],
                       foreground=THEME["text"],
                       font=('Segoe UI', 10),
                       rowheight=28)
        style.map("Treeview.Heading", background=[('active', THEME["secondary"])])
        style.map("Treeview", background=[('selected', THEME["primary"])],
                 foreground=[('selected', 'white')])

        # Header principal
        header = tk.Frame(self, bg=THEME["primary"])
        header.pack(fill=tk.X)
        tk.Label(header, text="Expediente Clínico", bg=THEME["primary"],
                fg="white", font=("Segoe UI", 20, "bold")).pack(pady=20)

        # Container principal
        main_container = tk.Frame(self, bg=THEME["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- PANEL IZQUIERDO ---
        frame_left = tk.Frame(main_container, bg=THEME["white"], width=350, relief=tk.FLAT, bd=1)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        tk.Label(frame_left, text="Directorio de Pacientes", bg=THEME["primary"],
                fg="white", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=(0, 10))

        # Scrollbar para pacientes
        scroll_pacientes = ttk.Scrollbar(frame_left, orient="vertical")
        scroll_pacientes.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

        self.tree_pacientes = ttk.Treeview(frame_left, columns=("ID", "Nombre"),
                                          show="headings", height=25,
                                          yscrollcommand=scroll_pacientes.set)
        self.tree_pacientes.heading("ID", text="ID")
        self.tree_pacientes.column("ID", width=50, anchor=tk.CENTER)
        self.tree_pacientes.heading("Nombre", text="Nombre Completo")
        self.tree_pacientes.column("Nombre", width=280)
        self.tree_pacientes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scroll_pacientes.config(command=self.tree_pacientes.yview)
        self.tree_pacientes.bind("<<TreeviewSelect>>", self._on_paciente_selected)

        # --- PANEL DERECHO ---
        frame_right = tk.Frame(main_container, bg=THEME["bg"])
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_paciente_seleccionado = tk.Label(frame_right, text="Seleccione un paciente",
                                                  bg=THEME["primary"], fg="white",
                                                  font=("Segoe UI", 12, "bold"), pady=10)
        self.lbl_paciente_seleccionado.pack(fill=tk.X, pady=(0, 10))

        # Historial
        frame_hist = tk.LabelFrame(frame_right, text="  Historial Médico (Doble clic para editar)  ",
                                   bg=THEME["bg"], fg=THEME["text"],
                                   font=("Segoe UI", 11, "bold"), bd=1, relief=tk.SOLID)
        frame_hist.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Scrollbar para historial
        scroll_hist = ttk.Scrollbar(frame_hist, orient="vertical")
        scroll_hist.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

        self.tree_historial = ttk.Treeview(frame_hist,
                                          columns=("ID_H", "Fecha", "Doctor", "Diag", "Trat"),
                                          show="headings", height=8,
                                          yscrollcommand=scroll_hist.set)
        self.tree_historial.heading("ID_H", text="ID")
        self.tree_historial.column("ID_H", width=40, anchor=tk.CENTER)
        self.tree_historial.heading("Fecha", text="Fecha")
        self.tree_historial.column("Fecha", width=100)
        self.tree_historial.heading("Doctor", text="Doctor")
        self.tree_historial.column("Doctor", width=120)
        self.tree_historial.heading("Diag", text="Diagnóstico")
        self.tree_historial.column("Diag", width=250)
        self.tree_historial.heading("Trat", text="Tratamiento")
        self.tree_historial.column("Trat", width=250)
        self.tree_historial.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scroll_hist.config(command=self.tree_historial.yview)

        self.tree_historial.bind("<<TreeviewSelect>>", self._on_historial_selected)

        # Formulario
        self.frame_form = tk.LabelFrame(frame_right, text="  Detalle de Consulta  ",
                                       bg=THEME["white"], fg=THEME["text"],
                                       font=("Segoe UI", 11, "bold"), bd=1, relief=tk.SOLID)
        self.frame_form.pack(fill=tk.X, pady=(0, 10))

        form_inner = tk.Frame(self.frame_form, bg=THEME["white"])
        form_inner.pack(padx=10, pady=10, fill=tk.BOTH)

        tk.Label(form_inner, text="Diagnóstico:", bg=THEME["white"],
                fg=THEME["text"], font=("Segoe UI", 10)).grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.txt_diag = tk.Text(form_inner, height=3, width=70, font=("Segoe UI", 10),
                               bg=THEME["white"], relief=tk.SOLID, bd=1)
        self.txt_diag.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_inner, text="Tratamiento:", bg=THEME["white"],
                fg=THEME["text"], font=("Segoe UI", 10)).grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.txt_trat = tk.Text(form_inner, height=3, width=70, font=("Segoe UI", 10),
                               bg=THEME["white"], relief=tk.SOLID, bd=1)
        self.txt_trat.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        form_inner.columnconfigure(1, weight=1)

        # --- BOTONES CRUD ---
        frame_btns = tk.Frame(self.frame_form, bg=THEME["white"])
        frame_btns.pack(pady=(0, 10))

        self.btn_guardar = tk.Button(frame_btns, text="Guardar Nuevo", bg=THEME["success"],
                                     fg="white", font=("Segoe UI", 9, "bold"), bd=0,
                                     padx=15, pady=8, cursor="hand2",
                                     command=lambda: self.controller.gestion_historial("crear"))
        self.btn_guardar.pack(side=tk.LEFT, padx=5)

        self.btn_editar = tk.Button(frame_btns, text="Actualizar", bg=THEME["info"],
                                    fg="white", font=("Segoe UI", 9, "bold"), bd=0,
                                    padx=15, pady=8, cursor="hand2",
                                    command=lambda: self.controller.gestion_historial("actualizar"))
        self.btn_editar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = tk.Button(frame_btns, text="Eliminar", bg=THEME["danger"],
                                      fg="white", font=("Segoe UI", 9, "bold"), bd=0,
                                      padx=15, pady=8, cursor="hand2",
                                      command=lambda: self.controller.gestion_historial("eliminar"))
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_btns, text="Limpiar", bg=THEME["accent"], fg="white",
                 font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8,
                 cursor="hand2", command=self.limpiar_form).pack(side=tk.LEFT, padx=5)

        if hasattr(self.controller, 'main_controller') and self.controller.main_controller:
            tk.Button(frame_btns, text="← Volver", bg=THEME["secondary"], fg="white",
                     font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8,
                     cursor="hand2", command=self.controller.main_controller.go_back_to_main_menu).pack(side=tk.LEFT, padx=5)

    # --- Eventos UI ---
    def _on_paciente_selected(self, event):
        sel = self.tree_pacientes.selection()
        if sel:
            item = self.tree_pacientes.item(sel[0])
            self.controller.seleccionar_paciente(item['values'][0], item['values'][1])

    def _on_historial_selected(self, event):
        sel = self.tree_historial.selection()
        if sel:
            item = self.tree_historial.item(sel[0])
            valores = item['values']
            # values = (ID_Historial, Fecha, Doctor, Diag, Trat)
            # Pasamos ID, Diagnostico y Tratamiento al controlador
            self.controller.seleccionar_registro_historial(valores[0], valores[3], valores[4])

    # --- Actualizaciones Visuales ---
    def actualizar_lista_pacientes(self, pacientes):
        self.tree_pacientes.delete(*self.tree_pacientes.get_children())
        for p in pacientes:
            self.tree_pacientes.insert("", "end", values=(p['ID_Paciente'], f"{p['Nombres']} {p['Apellidos']}"))

    def actualizar_historial(self, historial):
        self.tree_historial.delete(*self.tree_historial.get_children())
        for h in historial:
            self.tree_historial.insert("", "end", values=(h['ID_Historial'], h['Fecha_Registro'], h['Doctor'], h['Diagnostico'], h['Tratamiento']))

    def llenar_form(self, diag, trat):
        self.txt_diag.delete("1.0", tk.END)
        self.txt_diag.insert("1.0", diag)
        self.txt_trat.delete("1.0", tk.END)
        self.txt_trat.insert("1.0", trat)
        self.frame_form.config(text="  Editando Registro  ", fg=THEME["warning"])

    def limpiar_form(self):
        self.txt_diag.delete("1.0", tk.END)
        self.txt_trat.delete("1.0", tk.END)
        self.tree_historial.selection_remove(self.tree_historial.selection())
        self.controller.registro_seleccionado_id = None
        self.frame_form.config(text="  Detalle de Consulta (Nuevo)  ", fg=THEME["text"])