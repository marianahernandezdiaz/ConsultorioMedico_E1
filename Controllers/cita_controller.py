from Models.cita_Model import CitaModel
# Importar vistas
from Views.cita_view import CitaView
from Views.formCitas_view import FormularioCita

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
        
    def search_pacientes(self, term):
        return self.model.search_paciente(term)

    def agendar_cita(self, paciente_id, doctor_id, fecha, hora, motivo):
        # Aquí puedes añadir validaciones de negocio antes de llamar al modelo
        return self.model.create_cita(paciente_id, doctor_id, fecha, hora, motivo)
        
    # Nota: handle_modify_cita se dejará en el MainController para gestionar el flujo principal
    # pero aquí se podría añadir una versión simple si es necesario.