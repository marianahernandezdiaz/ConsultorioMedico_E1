from Models.user_model import UserModel
from Models.cita_Model import CitaModel # Importación CRÍTICA
from Views.login_view import LoginView # Asumiendo que existe
##from Views.main_menu_view import MainMenuView # Asumiendo que existe
from Controllers.cita_controller import CitaController
from tkinter import messagebox
import tkinter as tk # Necesario para la clase base del root

class MainController:
    """
    
    """
    
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()
        self.cita_model = CitaModel() # 🚨 INICIALIZACIÓN CRÍTICA para validación
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
            #self.show_main_menu(self.current_user['Nombre_Rol']) # Ir al menú RBAC
            self.open_citas_module() # Abrir módulo de citas automáticamente para pruebas
        else:
            self.login_view.show_error("Credenciales incorrectas o usuario no encontrado.")

    def show_main_menu(self, role):
        # Implementación mínima de RBAC
        options = []
        if role in ('Administrador', 'Recepcionista'):
             options.append(("Programación de Citas", self.open_citas_module))
        if role == 'Administrador':
            options.append(("Reportes de Ocupación", self.open_reportes_module))
        
        if not options:
             messagebox.showinfo("Acceso Denegado", "Su rol no tiene módulos asignados.")
             return
             
        # Limpiar la ventana y cargar el menú
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # self.main_menu_view = MainMenuView(self.root, self, options) # Suponiendo esta vista existe

    def open_citas_module(self):
        print("Abriendo Programación de Citas...")
        for widget in self.root.winfo_children():
            widget.destroy()
        # El CitaController automáticamente carga su vista (CitaView)
        self.cita_controller = CitaController(self.root, self)
        print("✅ Módulo de Programación de Citas cargado.")

    def open_reportes_module(self):
        print("Abriendo Reportes de Ocupación...")



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