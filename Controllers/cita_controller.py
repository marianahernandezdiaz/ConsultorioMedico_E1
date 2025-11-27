from Models.cita_Model import CitaModel
from Views.cita_view import CitaView

class CitaController:
    """Controlador para el módulo de Programación de Citas."""
    
    def __init__(self, master_view, main_controller):
        self.master_view = master_view
        self.main_controller = main_controller
        self.model = CitaModel()
        self.view = CitaView(master_view, self)
        


    def get_citas_for_day(self, date):
        """Solicita las citas para una fecha específica al modelo."""
        # Se asegura que la fecha se envíe en formato SQL (YYYY-MM-DD)
        return self.model.get_citas_by_day(date)

    def get_doctors_list(self):
        """Retorna la lista de doctores disponibles."""
        return self.model.get_all_doctors()
        
    def search_pacientes(self, term):
        """Realiza la búsqueda de pacientes para el agendamiento."""
        return self.model.search_paciente(term)

    def agendar_cita(self, paciente_id, doctor_id, fecha, hora, motivo):
        """Recibe datos de la vista y llama al modelo para crear la cita."""
        datos = (paciente_id, doctor_id, fecha, hora, motivo)
        if self.model.create_cita(datos):
            return True
        return False

    def modificar_cita(self, doctor_id, fecha, hora, estado, motivo, cita_id):
        """Recibe datos y llama al modelo para actualizar la cita."""
        datos = (doctor_id, fecha, hora, estado, motivo, cita_id)
        if self.model.update_cita(datos):
            return True
        return False