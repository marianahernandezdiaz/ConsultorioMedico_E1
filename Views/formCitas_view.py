import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys, os

# Para usar la misma paleta global del sistema
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME

PALETTE = THEME


class FormularioCita(tk.Toplevel):
    """
    Ventana modal para Agendar o Modificar Citas.
    """
    def __init__(self, master, cita_controller, cita_data=None):
        super().__init__(master)
        
        self.cita_controller = cita_controller 
        # Referencia al MainController (para la función de validación de modificar)
        self.main_controller = cita_controller.main_controller 
        
        self.cita_data = cita_data 
        self.is_modification = cita_data is not None
        
        # Variables de control
        self.paciente_id = None
        self.search_var = tk.StringVar()
        self.selected_doctor_id = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.time_var = tk.StringVar(value="10:00:00")
        self.motivo_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Agendada")

        self.title("Modificar Cita" if self.is_modification else "Agendar Nueva Cita")
        self.geometry("520x480")
        self.resizable(False, False)
        
        self.transient(master) 
        self.grab_set() 
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self._configure_styles()
        self._load_doctors()
        self._create_widgets()
        
        if self.is_modification:
            self._load_data_for_modification()
            
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Fondo general de la ventana
        self.configure(background=PALETTE["bg"]) 

        # Frame principal del formulario
        style.configure("CitaForm.TFrame", background=PALETTE["bg"])

        # Estilo para etiquetas y campos
        style.configure(
            "TLabel",
            background=PALETTE["bg"],
            foreground=PALETTE["text"],
            font=('Segoe UI', 10, 'bold')
        )
        style.configure(
            "CitaInfo.TLabel",
            background=PALETTE["bg"],
            foreground=PALETTE["text"],
            font=('Segoe UI', 9)
        )
        style.configure("TEntry", fieldbackground=PALETTE["white"])
        style.configure("TCombobox", fieldbackground=PALETTE["white"])

        # Botón de Guardar/Modificar
        style.configure(
            "CitaGuardar.TButton",
            background=PALETTE["success"],
            foreground="white",
            font=('Segoe UI', 10, 'bold'),
            padding=6
        )
        style.map(
            "CitaGuardar.TButton",
            background=[('active', PALETTE["primary"])],
            foreground=[('active', 'white')]
        )

    def _load_doctors(self):
        """Carga la lista de doctores desde el controlador para el ComboBox."""
        doctors = self.cita_controller.get_doctors_list()
        
        # Crea un mapa 'Nombre (ID:X)' -> ID
        self.doctor_map = {
            f"{d['Nombre_usuario']} (ID:{d['ID_Usuario']})": d['ID_Usuario']
            for d in doctors
        }
        self.doctor_options = list(self.doctor_map.keys())
        
        if not self.doctor_options:
            self.doctor_options = ["No hay doctores disponibles"]
            self.selected_doctor_id.set(self.doctor_options[0])
        else:
            self.selected_doctor_id.set(self.doctor_options[0])

    def _create_widgets(self):
        # ===== Header =====
        header = tk.Frame(self, bg=PALETTE["primary"])
        header.pack(fill="x")

        tk.Label(
            header,
            text="Modificar Cita" if self.is_modification else "Agendar Nueva Cita",
            bg=PALETTE["primary"],
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        # ===== Contenedor principal (fondo) =====
        outer = tk.Frame(self, bg=PALETTE["bg"])
        outer.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== Card del formulario =====
        main_frame = ttk.Frame(outer, padding="15", style="CitaForm.TFrame")
        main_frame.pack(fill='both', expand=True)

        # Usar grid para un layout más ordenado
        main_frame.columnconfigure(1, weight=1)

        row = 0
        
        # --- Campo Paciente (Búsqueda) ---
        ttk.Label(main_frame, text="Paciente (ID):", anchor='w').grid(
            row=row, column=0, sticky="w", pady=5, padx=5
        )
        self.search_entry = ttk.Entry(main_frame, textvariable=self.search_var)
        self.search_entry.grid(
            row=row, column=1, sticky="ew", pady=5, padx=5
        )
        self.search_button = ttk.Button(
            main_frame, text="Buscar", command=self._search_paciente
        )
        self.search_button.grid(
            row=row, column=2, sticky="e", pady=5, padx=5
        )
        row += 1
        
        # --- Info ID Paciente ---
        self.paciente_info_label = ttk.Label(
            main_frame,
            text="ID: (No seleccionado)",
            anchor='w',
            style="CitaInfo.TLabel"
        )
        self.paciente_info_label.grid(
            row=row, column=0, columnspan=3, sticky="w", padx=5
        )
        row += 1

        # --- Doctor Asignado ---
        ttk.Label(main_frame, text="Doctor Asignado:", anchor='w').grid(
            row=row, column=0, sticky="w", pady=5, padx=5
        )
        self.doctor_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.selected_doctor_id,
            values=self.doctor_options,
            state="readonly"
        )
        self.doctor_combobox.grid(
            row=row, column=1, columnspan=2, sticky="ew", pady=5, padx=5
        )
        row += 1

        # --- Fecha ---
        ttk.Label(main_frame, text="Fecha (YYYY-MM-DD):", anchor='w').grid(
            row=row, column=0, sticky="w", pady=5, padx=5
        )
        ttk.Entry(main_frame, textvariable=self.date_var).grid(
            row=row, column=1, columnspan=2, sticky="ew", pady=5, padx=5
        )
        row += 1

        # --- Hora ---
        ttk.Label(main_frame, text="Hora (HH:MM:SS):", anchor='w').grid(
            row=row, column=0, sticky="w", pady=5, padx=5
        )
        ttk.Entry(main_frame, textvariable=self.time_var).grid(
            row=row, column=1, columnspan=2, sticky="ew", pady=5, padx=5
        )
        row += 1

        # --- Motivo ---
        ttk.Label(main_frame, text="Motivo:", anchor='w').grid(
            row=row, column=0, sticky="w", pady=5, padx=5
        )
        ttk.Entry(main_frame, textvariable=self.motivo_var).grid(
            row=row, column=1, columnspan=2, sticky="ew", pady=5, padx=5
        )
        row += 1

        # --- Estado (Solo para Modificación) ---
        ttk.Label(main_frame, text="Estado:", anchor='w').grid(
            row=row, column=0, sticky="w", pady=5, padx=5
        )
        estado_options = ["Agendada", "Cancelada", "Completada"]
        self.estado_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.estado_var,
            values=estado_options,
            state="readonly"
        )
        self.estado_combobox.grid(
            row=row, column=1, columnspan=2, sticky="ew", pady=5, padx=5
        )
        row += 1
        
        # --- Botón Guardar ---
        button_text = "Guardar Modificación" if self.is_modification else "Agendar Cita"
        command = self._handle_modification if self.is_modification else self._handle_agendar
        
        ttk.Button(
            main_frame,
            text=button_text,
            command=command,
            style="CitaGuardar.TButton"
        ).grid(
            row=row, column=0, columnspan=3, pady=20, padx=5, sticky="ew"
        )

    # =========================================================
    # LÓGICA DE PRECARGA PARA MODIFICACIÓN
    # =========================================================
    def _load_data_for_modification(self):
        """Llena los campos del formulario con los datos de la cita a modificar."""
        data = self.cita_data
        
        # 1. Cargar información del PACIENTE
        self.paciente_id = data['ID_Paciente']
        patient_full_name = f"{data['Paciente_Nombre']} {data['Paciente_Apellido']}"
        
        self.search_var.set(patient_full_name) 
        self.paciente_info_label.config(text=f"ID: {self.paciente_id} | {patient_full_name}")
        
        # Deshabilitar la búsqueda de paciente en modo modificación
        self.search_entry.config(state='readonly')
        self.search_button.destroy() 

        # 2. Campos de texto y variables
        self.date_var.set(str(data['Fecha'])) 
        self.time_var.set(str(data['Hora'])[:5])  # Muestra solo HH:MM
        self.motivo_var.set(data['Motivo'])
        
        # 3. Doctor (Selecciona el correcto en el ComboBox)
        doctor_name_key = f"{data['Doctor_Nombre']} (ID:{data['Doctor_ID']})"
        if doctor_name_key in self.doctor_map:
            self.selected_doctor_id.set(doctor_name_key) 
        
        # 4. Establecer el estado inicial
        self.estado_var.set(data['Estado']) 

    # =========================================================
    # MANEJADORES DE OPERACIONES
    # =========================================================
    
    def _search_paciente(self):
        """Busca paciente por ID y permite seleccionar uno."""
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Advertencia", "Ingrese un ID de paciente.")
            return

        if not search_term.isdigit():
            messagebox.showwarning("ID inválido", "Debe ingresar un ID numérico de paciente.")
            self.paciente_id = None
            self.paciente_info_label.config(text="ID: (No seleccionado)")
            return

        # Llamar al controlador (por ID)
        paciente = self.cita_controller.search_paciente_by_id(int(search_term))
        # o si dejaste search_pacientes como wrapper por ID:
        # paciente = self.cita_controller.search_pacientes(search_term)

        if not paciente:
            messagebox.showinfo("Búsqueda", "No se encontró un paciente con ese ID.")
            self.paciente_id = None
            self.paciente_info_label.config(text="ID: (No seleccionado)")
            return

        # Aquí paciente YA es un dict, no lista
        self.paciente_id = paciente['ID_Paciente']
        full_name = f"{paciente['Nombres']} {paciente['Apellidos']}"
        self.paciente_info_label.config(text=f"ID: {self.paciente_id} | {full_name}")
        messagebox.showinfo("Éxito", f"Paciente seleccionado: {full_name}")


    def _handle_agendar(self):
        """Recoge los datos y llama al CitaController para agendar."""
        try:
            if not self.paciente_id:
                messagebox.showwarning("Error", "Debe seleccionar un paciente.")
                return
            
            doctor_key = self.selected_doctor_id.get()
            doctor_id = self.doctor_map.get(doctor_key)
            
            if not doctor_id:
                messagebox.showwarning("Error", "Debe seleccionar un doctor válido.")
                return

            success = self.cita_controller.agendar_cita(
                paciente_id=self.paciente_id,
                doctor_id=doctor_id,
                fecha=self.date_var.get(),
                hora=self.time_var.get(),
                motivo=self.motivo_var.get()
            )
            
            if success:
                messagebox.showinfo("Éxito", "Cita agendada correctamente.")
                self.destroy()
                # Recargar la agenda principal
                self.cita_controller.view.load_agenda(self.date_var.get()) 
            else:
                messagebox.showerror("Error", "Error al agendar la cita.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            
            
    # views/formCitas_view.py (Método _handle_modification)

    def _handle_modification(self):
        """Recoge los datos, valida tipos y llama al MainController."""
        
        # --- 1. Extracción y Conversión de IDs (Asegurando INT) ---
        doctor_key = self.selected_doctor_id.get()
        if not doctor_key or doctor_key == "No hay doctores disponibles":
            messagebox.showwarning("Error", "Debe seleccionar un doctor válido.")
            return

        doctor_id_str = self.doctor_map.get(doctor_key)
        doctor_id = int(doctor_id_str) 
        cita_id = int(self.cita_data['ID_Cita']) 

        # --- 2. Corrección del Formato de Hora ---
        new_hora_raw = self.time_var.get()
            
        # Si el formato es HH:MM (5 caracteres), le añadimos los segundos (:00)
        if len(new_hora_raw) == 5: 
            new_hora = new_hora_raw + ":00" 
        else:
            new_hora = new_hora_raw
                
        # --- 3. Recoger el resto de valores ---
        new_fecha = self.date_var.get()
        new_motivo = self.motivo_var.get()
        new_estado = self.estado_var.get()
            
        # ... (Validaciones adicionales aquí)

        # Llamada al controlador principal
        self.cita_controller.handle_modify_cita(
            cita_id=cita_id,
            id_doctor=doctor_id,
            new_fecha=new_fecha,
            new_hora=new_hora, 
            new_motivo=new_motivo,
            new_estado=new_estado,
            form_view=self 
        )
            
    def destroy(self):
        self.grab_release()
        super().destroy()
