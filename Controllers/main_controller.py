from Models.user_model import UserModel
from Views.login_view import LoginView
from Controllers.doctor_controller import DoctorController
from Models.cita_Model import CitaModel # Importación CRÍTICA
from Views.login_view import LoginView 
from Views.menu_view import MainMenuView
from Views.GPacientes.PacientesMenuPrincipal import PacientesMenuPrincipal
from Controllers.cita_controller import CitaController
from tkinter import messagebox
import tkinter as tk # Necesario para la clase base del root

class MainController:
    """
    
    """
    
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()
        self.cita_model = CitaModel()
        self.current_user = None 
        
        self.root.geometry("1x1") 
        self.root.withdraw() 
        self.show_login()
    
    def show_login(self):
        self.root.deiconify() 
        for widget in self.root.winfo_children():
            widget.destroy()
        self.login_view = LoginView(self.root, self)
        
    def handle_login(self, email, password):
        user_data = self.user_model.get_user_by_credentials(email, password)
        
        if user_data:
            self.current_user = user_data
            self.login_view.destroy() 
            print(f"✅ Login exitoso. Rol: {self.current_user['Nombre_Rol']}")
            self.show_main_menu(self.current_user['Nombre_Rol']) # Ir al menú RBAC
        else:
            self.login_view.show_error("Credenciales incorrectas o usuario no encontrado.")

    def show_main_menu(self, role):
        """
        Carga la vista del menú principal o el módulo directo según el rol.
        Aquí se implementa el Control de Acceso Basado en Roles (RBAC).
        """
        # Nota: Por ahora, solo mostraremos un mensaje, 
        # pero aquí cargarías la clase views.main_menu_view.py
        print(f"--- Cargando Menú Principal para {role} ---")
        
        # Ejemplo de lógica de ruteo:
        if role == 'Doctor':
            # Si es Doctor, puede que queramos llevarlo directamente a su módulo de Expediente.
            self.doctor_controller = DoctorController(self.root, self.current_user)
            print("Abriendo Módulo de Expediente Clínico...")
            # Aquí se crearía una instancia de views.expediente_view
        else:
            # Para Administrador y Recepcionista, cargamos el menú con opciones.
            # Aquí se crearía una instancia de views.main_menu_view
            print(f"Cargando menú con opciones permitidas para {role}...")

    # --- Métodos de Enrutamiento (Stubs) ---
    # Estos métodos serían llamados por los botones en main_menu_view
    
            """
            Implementa el Control de Acceso Basado en Roles (RBAC) 
            y carga la vista del menú principal.
            """
            options = []

            # 1. Gestión de Pacientes (Administrador, Recepcionista)
            if role in ('Administrador', 'Recepcionista'):
                options.append(("1. Gestión de Pacientes", self.open_pacientes_module))
                
            # 2. Programación de Citas (Recepcionista)
            if role == 'Recepcionista':
                options.append(("2. Programación de Citas", self.open_citas_module))
                
            # 3. Expediente Clínico (Doctor)
            if role == 'Doctor':
                options.append(("3. Expediente Clínico", self.open_expediente_module))

            # 4. Facturación y Pagos (Administrador, Recepcionista)
            if role in ('Administrador', 'Recepcionista'):
                options.append(("4. Facturación y Pagos", self.open_facturacion_module))

            # 5. Reportes de Ocupación (Administrador)
            if role == 'Administrador':
                options.append(("5. Reportes de Ocupación", self.open_reportes_module))
                
            if not options:
                messagebox.showinfo("Acceso Denegado", "Su rol no tiene módulos asignados.")
                return
                
            # Limpiar la ventana y cargar el menú
            for widget in self.root.winfo_children():
                widget.destroy()
            

            self.Menu_view = MainMenuView(self.root, self, options, role) 


        # ----------------------------------------------------
        # MÉTODOS DE ACCESO A MÓDULOS (Endpoints para los botones)
        # ----------------------------------------------------

    def open_pacientes_module(self):
        print("Abriendo Módulo de Gestión de Pacientes...")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.PacientesMenuPrincipal = PacientesMenuPrincipal()
        print("✅ Módulo de Programación de Citas cargado.")


    def open_citas_module(self):
        print("Abriendo Programación de Citas...")
        for widget in self.root.winfo_children():
            widget.destroy()
            # El CitaController automáticamente carga su vista (CitaView)
        self.cita_controller = CitaController(self.root, self)
        print("✅ Módulo de Programación de Citas cargado.")

    def open_expediente_module(self):
        print("Abriendo Módulo de Expediente Clínico...")
        # Aquí iría la lógica para cargar el ExpedienteController
            
    def open_facturacion_module(self):
        print("Abriendo Módulo de Facturación y Pagos...")
        # Aquí iría la lógica para cargar el FacturacionController

    def open_reportes_module(self):
        print("Abriendo Reportes de Ocupación...")
        # Aquí iría la lógica para cargar el ReportesController


    def handle_modify_cita(self, cita_id, id_doctor, new_fecha, new_hora, new_motivo, new_estado, form_view):
        """
        Valida el horario con el modelo y realiza la modificación de la cita.
        """
        
        # 1. Validación de conflicto
        # Usamos self.cita_model, que inicializamos en __init__
        is_conflict = self.cita_model.check_cita_conflict(
            id_cita_to_exclude=cita_id,
            id_doctor=id_doctor,
            fecha=new_fecha,
            hora=new_hora
        )
        
        if is_conflict:
            messagebox.showerror(
                "Error de Agenda", 
                f"El Doctor ya tiene una cita agendada el día {new_fecha} a las {new_hora}."
            )
            return

        # 2. Modificación de la cita
        
        success = self.cita_model.update_cita(
                cita_id=cita_id,
                id_doctor=id_doctor,
                fecha=new_fecha,
                hora=new_hora,
                motivo=new_motivo,
                estado=new_estado
            )
            
        if success:
            messagebox.showinfo("Éxito", "Cita modificada correctamente.")
            form_view.destroy() # Cerrar la ventana modal
                
            if hasattr(self, 'cita_controller') and hasattr(self.cita_controller, 'view'):
                # 1. Actualizar el valor de la variable de fecha en la vista (opcional, pero limpia)
                agenda_view = self.cita_controller.view
                
                form_view.destroy()
                
                agenda_view.date_var.set(new_fecha)
                
                self.root.after(50, lambda: agenda_view.load_agenda(new_fecha))
        
                # 2. Llamar al método de recarga (que ahora usará la fecha actualizada)
                self.cita_controller.view.load_agenda(new_fecha) 
            else:
        # Esto ocurre si modificamos una cita sin que la agenda principal esté abierta
                 messagebox.showwarning("Advertencia", "La cita se modificó, pero la agenda principal debe recargarse manualmente.")
                
              
        else:
                messagebox.showerror("Error", "No se pudo modificar la cita.")


    def __del__(self):
        if self.user_model:
            self.user_model.db.close()
        if self.cita_model:
            self.cita_model.db.close()