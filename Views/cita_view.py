import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Views.formCitas_view import FormularioCita
import calendar
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME

class CitaView(ttk.Frame):
    """
    Interfaz principal para la Programación de Citas (Agenda).
    Muestra la agenda y permite agendar/modificar.
    """
    def __init__(self, master, controller):
        super().__init__(master, padding="0")

        self.master = master
        self.controller = controller

        self.master.title("Programación de Citas")
        self.master.geometry("1100x650")
        self.master.config(bg=THEME["bg"])
        self.pack(expand=True, fill='both')

        self._configure_styles()

        # Inicialización de la variable de fecha antes de crear widgets
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        self._create_widgets()

        # Cargar datos iniciales
        self.load_agenda(self.date_var.get()) 

    def _configure_styles(self):
        """Configura estilos básicos usando la paleta minimalista."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Cita.TFrame", background=THEME["bg"])
        style.configure("TFrame", background=THEME["bg"])
        style.configure("TLabel", background=THEME["bg"], foreground=THEME["text"], font=('Segoe UI', 10))

        # Estilos para Treeview
        style.configure("Treeview",
                       background=THEME["white"],
                       fieldbackground=THEME["white"],
                       foreground=THEME["text"],
                       font=('Segoe UI', 10),
                       rowheight=30,
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       font=('Segoe UI', 10, 'bold'),
                       background=THEME["primary"],
                       foreground="white",
                       borderwidth=0)
        style.map("Treeview.Heading", background=[('active', THEME["secondary"])])
        style.map("Treeview", background=[('selected', THEME["primary"])],
                 foreground=[('selected', 'white')])

        # Botones
        style.configure("Accent.TButton",
                       background=THEME["primary"],
                       foreground="white",
                       font=('Segoe UI', 10),
                       padding=10,
                       borderwidth=0)
        style.map("Accent.TButton", background=[('active', THEME["secondary"])])

        style.configure("Secondary.TButton",
                       background=THEME["accent"],
                       foreground="white",
                       font=('Segoe UI', 10),
                       padding=8)
        style.map("Secondary.TButton", background=[('active', THEME["secondary"])])


    def _create_widgets(self):
        """Define el layout de la ventana (Selector de Fecha y Tabla de Citas)."""

        # Header
        header = tk.Frame(self, bg=THEME["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Programación de Citas", bg=THEME["primary"],
                fg="white", font=("Segoe UI", 20, "bold")).pack(pady=20)

        # Container principal
        main_container = ttk.Frame(self, style="Cita.TFrame")
        main_container.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        # --- Panel Superior (Control de Fecha y Botones) ---
        control_frame = ttk.Frame(main_container, style="Cita.TFrame")
        control_frame.pack(side="top", fill="x", pady=(0, 15))

        # Frame para fecha
        date_frame = ttk.Frame(control_frame, style="Cita.TFrame")
        date_frame.pack(side="left")

        ttk.Label(date_frame, text="Fecha:", font=('Segoe UI', 10, 'bold')).pack(side="left", padx=(0, 5))
        date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=15, font=('Segoe UI', 10))
        date_entry.pack(side="left", padx=5, ipady=5)

        ttk.Button(date_frame, text="Mostrar", style="Accent.TButton",
                  command=self._handle_load_agenda, cursor="hand2").pack(side="left", padx=5)

        ttk.Button(date_frame, text="Recargar", style="Accent.TButton",
                  command=self._handle_load_agenda, cursor="hand2").pack(side="left", padx=5)

        # Botones derecha
        btn_frame = ttk.Frame(control_frame, style="Cita.TFrame")
        btn_frame.pack(side="right")

        ttk.Button(btn_frame, text="+ Agendar Cita", style="Accent.TButton",
                  command=self._open_agendar_form, cursor="hand2").pack(side="left", padx=5)

        if hasattr(self.controller, 'main_controller') and self.controller.main_controller:
            ttk.Button(btn_frame, text="← Volver", style="Secondary.TButton",
                      command=self.controller.main_controller.go_back_to_main_menu,
                      cursor="hand2").pack(side="left", padx=5)

        # --- Tabla de Citas (Agenda) ---
        tree_frame = ttk.Frame(main_container)
        tree_frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.agenda_tree = ttk.Treeview(tree_frame,
                                        columns=('Hora', 'Paciente', 'Doctor', 'Motivo', 'Estado'),
                                        show='headings',
                                        yscrollcommand=scrollbar.set)
        self.agenda_tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.agenda_tree.yview)

        self.agenda_tree.heading('Hora', text='Hora')
        self.agenda_tree.heading('Paciente', text='Paciente')
        self.agenda_tree.heading('Doctor', text='Doctor')
        self.agenda_tree.heading('Motivo', text='Motivo')
        self.agenda_tree.heading('Estado', text='Estado')

        self.agenda_tree.column('Hora', width=80, anchor=tk.CENTER)
        self.agenda_tree.column('Paciente', width=200)
        self.agenda_tree.column('Doctor', width=150)
        self.agenda_tree.column('Motivo', width=250)
        self.agenda_tree.column('Estado', width=100, anchor=tk.CENTER)

        self.agenda_tree.bind('<Double-1>', self._handle_modify_cita)

    # --- Manejadores de Eventos ---

    def _handle_load_agenda(self):
        """Función que se llama al presionar 'Mostrar Agenda' o 'Recargar'."""
        date_str = self.date_var.get()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            self.load_agenda(date_str)
        except ValueError:
            messagebox.showerror("Error de Fecha", "El formato de fecha debe ser YYYY-MM-DD.")
            
    def load_agenda(self, date):
        """Carga los datos de las citas desde el controlador y los muestra en el Treeview."""
        
        
        self.date_var.set(date) 
        
        # Limpiar datos previos
        for item in self.agenda_tree.get_children():
            self.agenda_tree.delete(item)
            
        # Obtener citas del controlador
        citas = self.controller.get_citas_for_day(date)
        
        if citas:
            for cita in citas:
                # Insertar los datos en el Treeview
                self.agenda_tree.insert('', tk.END, 
                    values=(
                        str(cita['Hora'])[:5], # Formato HH:MM
                        f"{cita['Paciente_Nombre']} {cita['Paciente_Apellido']}",
                        cita['Doctor_Nombre'],
                        cita['Motivo'],
                        cita['Estado']
                    ),
                    tags=(cita['ID_Cita'],) # Almacenamos el ID de la cita
                )
        else:
            self.agenda_tree.insert('', tk.END, values=('', 'No hay citas para este día.', '', '', ''), tags=('empty',))
            
    def _open_agendar_form(self):
        """Abre una ventana modal para agendar una nueva cita."""
        FormularioCita(self.master, self.controller)


    def _handle_modify_cita(self, event):
        """Abre el formulario para modificar la cita seleccionada (doble clic)."""
        selected_item = self.agenda_tree.selection()
        if selected_item:
            item_id = self.agenda_tree.item(selected_item, 'tags')[0]
            if item_id != 'empty':
                cita_id_int = int(item_id)
                
                # Obtener los datos REALES de la BD antes de abrir el formulario
                cita_details = self.controller.get_cita_details(cita_id_int) 
                
                if cita_details:
                    FormularioCita(self.master, self.controller, cita_data=cita_details)
                else:
                    messagebox.showerror("Error", "No se pudieron obtener los detalles de la cita.")