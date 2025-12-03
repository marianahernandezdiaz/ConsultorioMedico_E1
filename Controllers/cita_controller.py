from tkinter import messagebox
from Models.cita_Model import CitaModel
from Views.cita_view import CitaView
from Views.formCitas_view import FormularioCita
import tkinter as tk # Necesario para root.after

class CitaController:
    """Controlador para el módulo de Programación de Citas."""
    
    def __init__(self, master_view, main_controller):
        self.master_view = master_view
        self.main_controller = main_controller
        self.model = CitaModel()
        
        # Cargar la vista principal de Citas (la agenda)
        self.view = CitaView(master_view, self) 

    def get_citas_for_day(self, date):
        return self.model.get_citas_by_day(date)
        
    def get_cita_details(self, cita_id):
        # Llama al modelo para obtener todos los detalles de la cita para la precarga
        return self.model.get_cita_details(cita_id)

    def get_doctors_list(self):
        return self.model.get_all_doctors()
        
    def search_paciente_by_id(self, term):
        # term viene como string, aquí lo convertimos a ID
        try:
            id_paciente = int(term)
        except ValueError:
            return None
        return self.model.obtener_paciente_por_id(id_paciente)


    def agendar_cita(self, paciente_id, doctor_id, fecha, hora, motivo):
        # Aquí puedes añadir validaciones de negocio antes de llamar al modelo
        return self.model.create_cita(paciente_id, doctor_id, fecha, hora, motivo)
        
    def handle_modify_cita(self, cita_id, id_doctor, new_fecha, new_hora, new_motivo, new_estado, form_view):
        """
        Valida el horario, realiza la modificación de la cita 
        y programa la recarga asíncrona de la agenda.
        """
        
        # 1. Validación de conflicto
        is_conflict = self.model.check_cita_conflict(
            id_cita_to_exclude=cita_id, id_doctor=id_doctor, fecha=new_fecha, hora=new_hora
        )
        
        if is_conflict:
            messagebox.showerror("Error de Agenda", f"El Doctor ya tiene una cita agendada el día {new_fecha} a las {new_hora}.")
            return

        # 2. Modificación de la cita
        success = self.model.update_cita(
                cita_id=cita_id, id_doctor=id_doctor, fecha=new_fecha, hora=new_hora, 
                motivo=new_motivo, estado=new_estado
            )
            
        # 3. Manejo de Resultado y Sincronización
        if success:
            
            # Definimos la función de acción segura
            def safe_reload_and_close():
                # self.view es la instancia de CitaView
                self.view.date_var.set(new_fecha) 
                self.view.load_agenda(new_fecha)
                form_view.destroy() # Cierra el formulario DESPUÉS de la recarga
                
            # Programamos la ejecución asíncrona para que no interfiera con el cierre del modal
            self.master_view.after(50, safe_reload_and_close) # 🚨 Usamos master_view (root) para el after
            messagebox.showinfo("Éxito", "Cita modificada correctamente.")

        else:
            messagebox.showerror("Error", "No se pudo modificar la cita.")