import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Views.formCitas_view import FormularioCita
import calendar 

class CitaView(ttk.Frame):
    """
    Interfaz principal para la Programación de Citas (Agenda).
    Muestra la agenda y permite agendar/modificar.
    """
    def __init__(self, master, controller):
        super().__init__(master, padding="15")
        
        self.master = master
        self.controller = controller
        
        self.master.title("Módulo de Programación de Citas")
        self.master.geometry("1000x600")
        self.pack(expand=True, fill='both')

        self._configure_styles()
        
        # Inicialización de la variable de fecha antes de crear widgets
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        
        self._create_widgets()
        
        # Cargar datos iniciales
        self.load_agenda(self.date_var.get()) 

    def _configure_styles(self):
        """Configura estilos básicos usando tu paleta de colores."""
        style = ttk.Style()
        # Colores de tu paleta
        style.configure("Cita.TFrame", background="#B2D9C4") 
        style.configure("Treeview", background="white", fieldbackground="white", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#44916F", foreground="white")
        style.map("Treeview.Heading", background=[('active', '#247D7F')]) 
        style.configure("Accent.TButton", background="#44916F", foreground="white", font=('Arial', 10, 'bold'))
        style.map("Accent.TButton", background=[('active', '#247D7F')])


    def _create_widgets(self):
        """Define el layout de la ventana (Selector de Fecha y Tabla de Citas)."""
        
        agenda_frame = ttk.Frame(self, padding="10", style="Cita.TFrame")
        agenda_frame.pack(side="top", fill="both", expand=True)
        
        # --- Panel Superior (Control de Fecha y Botones) ---
        control_frame = ttk.Frame(agenda_frame, padding="10", style="Cita.TFrame")
        control_frame.pack(side="top", fill="x")
        
        ttk.Label(control_frame, text="Seleccionar Fecha:", font=('Arial', 10, 'bold'), background="#B2D9C4").pack(side="left", padx=5)
        
        # Entrada de Fecha
        date_entry = ttk.Entry(control_frame, textvariable=self.date_var, width=12)
        date_entry.pack(side="left", padx=5)
        
        # Botón 1: Mostrar Agenda (llama a la recarga)
        ttk.Button(control_frame, text="Mostrar Agenda", command=self._handle_load_agenda).pack(side="left", padx=10)
        
        # Botón 2: Recargar (llama al mismo manejador)
        ttk.Button(control_frame, 
                   text="↺ Recargar", 
                   command=self._handle_load_agenda,
                   style="Accent.TButton").pack(side="left", padx=5)
        
        # Botón 3: Agendar nueva cita
        ttk.Button(control_frame, text="➕ Agendar Cita", style="Accent.TButton", command=self._open_agendar_form).pack(side="right", padx=10)
        
        # --- Tabla de Citas (Agenda) ---
        self.agenda_tree = ttk.Treeview(agenda_frame, 
                                        columns=('Hora', 'Paciente', 'Doctor', 'Motivo', 'Estado'), 
                                        show='headings')
        self.agenda_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.agenda_tree.heading('Hora', text='Hora')
        self.agenda_tree.heading('Paciente', text='Paciente')
        self.agenda_tree.heading('Doctor', text='Doctor')
        self.agenda_tree.heading('Motivo', text='Motivo')
        self.agenda_tree.heading('Estado', text='Estado')
        
        self.agenda_tree.column('Hora', width=80, anchor=tk.CENTER)
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
        
        # 🚨 CORRECCIÓN CLAVE: Sincroniza la variable de control de la interfaz
        # Esto es vital cuando el MainController llama a esta función con 'new_fecha'
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