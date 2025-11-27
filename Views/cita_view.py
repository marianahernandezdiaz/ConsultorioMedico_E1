import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar # Usaremos esto para el selector de fecha

class CitaView(ttk.Frame):
    """
    Interfaz principal para la Programación de Citas.
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
        self._create_widgets()
        
        # Cargar datos iniciales
        self.load_agenda(datetime.now().strftime("%Y-%m-%d")) # Carga la agenda del día actual

    def _configure_styles(self):
        """Configura estilos básicos para la vista de la agenda."""
        style = ttk.Style()
        # Puedes añadir estilos específicos aquí si usas tu paleta de colores
        style.configure("Agenda.TFrame", background="#EFEFEF")
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

    def _create_widgets(self):
        """Define el layout de la ventana (Selector de Fecha y Tabla de Citas)."""
        
        # Contenedor principal para la agenda
        agenda_frame = ttk.Frame(self, style="Agenda.TFrame")
        agenda_frame.pack(side="top", fill="both", expand=True)
        
        # --- Panel Superior (Control de Fecha y Botón Agendar) ---
        control_frame = ttk.Frame(agenda_frame, padding="10")
        control_frame.pack(side="top", fill="x")
        
        ttk.Label(control_frame, text="Seleccionar Fecha:", font=('Arial', 10, 'bold')).pack(side="left", padx=5)
        
        # Selector de Fecha (usaremos un Entry simple por ahora)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(control_frame, textvariable=self.date_var, width=12)
        date_entry.pack(side="left", padx=5)
        
        # Botón para cargar la agenda del día
        ttk.Button(control_frame, text="Mostrar Agenda", command=self._handle_load_agenda).pack(side="left", padx=10)
        
        # Botón para agendar nueva cita
        ttk.Button(control_frame, text="➕ Agendar Cita", command=self._open_agendar_form).pack(side="right", padx=10)
        
        # --- Tabla de Citas (Agenda) ---
        self.agenda_tree = ttk.Treeview(agenda_frame, 
                                        columns=('Hora', 'Paciente', 'Doctor', 'Motivo', 'Estado'), 
                                        show='headings')
        self.agenda_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Definir encabezados de columna
        self.agenda_tree.heading('Hora', text='Hora')
        self.agenda_tree.heading('Paciente', text='Paciente')
        self.agenda_tree.heading('Doctor', text='Doctor')
        self.agenda_tree.heading('Motivo', text='Motivo')
        self.agenda_tree.heading('Estado', text='Estado')
        
        # Configurar anchos (Opcional)
        self.agenda_tree.column('Hora', width=80, anchor=tk.CENTER)
        self.agenda_tree.column('Estado', width=100, anchor=tk.CENTER)
        
        # Enlazar evento de doble clic para modificar
        self.agenda_tree.bind('<Double-1>', self._handle_modify_cita)

    # --- Manejadores de Eventos ---

    def _handle_load_agenda(self):
        """Función que se llama al presionar 'Mostrar Agenda'."""
        date_str = self.date_var.get()
        try:
            # Validar formato de fecha (YYYY-MM-DD)
            datetime.strptime(date_str, "%Y-%m-%d")
            self.load_agenda(date_str)
        except ValueError:
            messagebox.showerror("Error de Fecha", "El formato de fecha debe ser YYYY-MM-DD.")
            
    def load_agenda(self, date):
        """Carga los datos de las citas desde el controlador y los muestra en el Treeview."""
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
                        cita['Hora'], 
                        f"{cita['Paciente_Nombre']} {cita['Paciente_Apellido']}",
                        cita['Doctor_Nombre'],
                        cita['Motivo'],
                        cita['Estado']
                    ),
                    tags=(cita['ID_Cita'],) # Almacenamos el ID de la cita en un tag para futuras modificaciones
                )
        else:
            self.agenda_tree.insert('', tk.END, values=('', 'No hay citas para este día.', '', '', ''), tags=('empty',))
            
    def _open_agendar_form(self):
        """Abre una ventana modal para agendar una nueva cita."""
        # Necesitamos una clase FormularioCita que herede de Toplevel
        messagebox.showinfo("Formulario de Agendamiento", "Aquí se abriría el formulario para crear la cita.")
        # Se llamaría a FormularioCita(self.master, self.controller)

    def _handle_modify_cita(self, event):
        """Abre el formulario para modificar la cita seleccionada (doble clic)."""
        selected_item = self.agenda_tree.selection()
        if selected_item:
            # Obtener el ID de la cita almacenado en el tag
            item_id = self.agenda_tree.item(selected_item, 'tags')[0]
            if item_id != 'empty':
                 messagebox.showinfo("Modificar Cita", f"Abriendo formulario para modificar la Cita ID: {item_id}")
                 # Aquí se llamaría a FormularioCita(self.master, self.controller, cita_id=item_id)