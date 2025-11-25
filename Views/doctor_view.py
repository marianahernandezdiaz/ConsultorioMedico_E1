import tkinter as tk
from tkinter import ttk

# --- PALETA DE COLORES ---
COLOR_FONDO = "#B2D9C4"       
COLOR_PANEL_IZQ = "#44916F"   
COLOR_TITULOS = "#247D7F"     
COLOR_INFO = "#80B9C8"        
COLOR_BTN = "#C29470"
COLOR_BTN_DANGER = "#A94442" # Rojo oscuro para eliminar
COLOR_BTN_EDIT = "#E0A800"   # Amarillo/Dorado para editar

class DoctorView(tk.Frame):
    def __init__(self, master, controller, doctor_name):
        super().__init__(master)
        self.controller = controller
        self.master = master
        
        self.configure(bg=COLOR_FONDO)
        self.pack(fill=tk.BOTH, expand=True)
        self.master.title(f"Sistema Médico - Expediente - {doctor_name}")
        self.master.geometry("1150x680")

        self._create_ui()

    def _create_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background=COLOR_TITULOS, foreground="white", font=('Arial', 10, 'bold'))
        style.configure("Treeview", rowheight=25)

        # --- PANEL IZQUIERDO ---
        frame_left = tk.Frame(self, bg=COLOR_PANEL_IZQ, width=350)
        frame_left.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(frame_left, text="Directorio Pacientes", bg=COLOR_PANEL_IZQ, fg="white", font=("Arial", 12, "bold")).pack(pady=15)

        self.tree_pacientes = ttk.Treeview(frame_left, columns=("ID", "Nombre"), show="headings", height=20)
        self.tree_pacientes.heading("ID", text="ID"); self.tree_pacientes.column("ID", width=40)
        self.tree_pacientes.heading("Nombre", text="Nombre Completo"); self.tree_pacientes.column("Nombre", width=200)
        self.tree_pacientes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree_pacientes.bind("<<TreeviewSelect>>", self._on_paciente_selected)

        # --- PANEL DERECHO ---
        frame_right = tk.Frame(self, bg=COLOR_FONDO)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.lbl_paciente_seleccionado = tk.Label(frame_right, text="Seleccione un paciente", bg=COLOR_INFO, font=("Arial", 12, "bold"), pady=5)
        self.lbl_paciente_seleccionado.pack(fill=tk.X, pady=5)

        # Historial
        frame_hist = tk.LabelFrame(frame_right, text="Historial Médico (Seleccione para editar)", bg=COLOR_FONDO, fg=COLOR_TITULOS, font=("Arial", 10, "bold"))
        frame_hist.pack(fill=tk.BOTH, expand=True, pady=10)

        # OJO: Agregamos columna ID_Historial oculta o visible para control interno
        self.tree_historial = ttk.Treeview(frame_hist, columns=("ID_H", "Fecha", "Doctor", "Diag", "Trat"), show="headings", height=6)
        self.tree_historial.heading("ID_H", text="ID"); self.tree_historial.column("ID_H", width=30)
        self.tree_historial.heading("Fecha", text="Fecha"); self.tree_historial.column("Fecha", width=100)
        self.tree_historial.heading("Doctor", text="Doctor"); self.tree_historial.column("Doctor", width=100)
        self.tree_historial.heading("Diag", text="Diagnóstico"); self.tree_historial.column("Diag", width=200)
        self.tree_historial.heading("Trat", text="Tratamiento"); self.tree_historial.column("Trat", width=200)
        self.tree_historial.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Binding para seleccionar un registro del historial
        self.tree_historial.bind("<<TreeviewSelect>>", self._on_historial_selected)

        # Formulario
        self.frame_form = tk.LabelFrame(frame_right, text="Detalle de Consulta", bg=COLOR_TITULOS, fg="white", font=("Arial", 10, "bold"))
        self.frame_form.pack(fill=tk.X, pady=5)

        tk.Label(self.frame_form, text="Diagnóstico:", bg=COLOR_TITULOS, fg="white").grid(row=0, column=0, sticky="ne", padx=5, pady=5)
        self.txt_diag = tk.Text(self.frame_form, height=3, width=60)
        self.txt_diag.grid(row=0, column=1, padx=5, pady=5, columnspan=3)

        tk.Label(self.frame_form, text="Tratamiento:", bg=COLOR_TITULOS, fg="white").grid(row=1, column=0, sticky="ne", padx=5, pady=5)
        self.txt_trat = tk.Text(self.frame_form, height=3, width=60)
        self.txt_trat.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

        # --- BOTONES CRUD ---
        frame_btns = tk.Frame(self.frame_form, bg=COLOR_TITULOS)
        frame_btns.grid(row=2, column=1, pady=10, sticky="w")

        # Botón Guardar Nuevo
        self.btn_guardar = tk.Button(frame_btns, text="GUARDAR NUEVO", bg=COLOR_BTN, fg="white", font=("Arial", 9, "bold"), 
                                     command=lambda: self.controller.gestion_historial("crear"))
        self.btn_guardar.pack(side=tk.LEFT, padx=5)

        # Botón Actualizar (Inicialmente deshabilitado visualmente)
        self.btn_editar = tk.Button(frame_btns, text="ACTUALIZAR", bg=COLOR_BTN_EDIT, fg="white", font=("Arial", 9, "bold"), 
                                    command=lambda: self.controller.gestion_historial("actualizar"))
        self.btn_editar.pack(side=tk.LEFT, padx=5)

        # Botón Eliminar
        self.btn_eliminar = tk.Button(frame_btns, text="ELIMINAR", bg=COLOR_BTN_DANGER, fg="white", font=("Arial", 9, "bold"), 
                                      command=lambda: self.controller.gestion_historial("eliminar"))
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Botón Limpiar
        tk.Button(frame_btns, text="Limpiar / Cancelar", command=self.limpiar_form).pack(side=tk.LEFT, padx=20)

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
        # Cambiamos color de fondo para indicar modo edición
        self.frame_form.config(text="EDITANDO REGISTRO EXISTENTE", fg=COLOR_BTN_EDIT)

    def limpiar_form(self):
        self.txt_diag.delete("1.0", tk.END)
        self.txt_trat.delete("1.0", tk.END)
        self.tree_historial.selection_remove(self.tree_historial.selection())
        self.controller.registro_seleccionado_id = None # Reseteamos ID en controller
        self.frame_form.config(text="Detalle de Consulta (Nuevo)", fg="white")