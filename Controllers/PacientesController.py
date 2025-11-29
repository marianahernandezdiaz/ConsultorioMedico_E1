# Controllers/PacientesController.py

from Models.GestionPacientesModel import GestionPacientesModel


class PacienteController:
    def __init__(self):
        self.model = GestionPacientesModel()

    def insertar_paciente(self, datos_formulario):
        """
        Recibe los datos de la vista InsertarPaciente y los manda al modelo.
        datos_formulario debe tener:
            - nombres
            - apellidos
            - fecha_nac
            - telefono
            - direccion
            - seguro_med
        """
        nuevo_id = self.model.insertar_paciente(datos_formulario)
        print(f">>> Paciente insertado con ID: {nuevo_id}")
        return nuevo_id


    def obtener_paciente_por_id(self, id_paciente: int):
        """
        Pide al modelo los datos de un paciente por su ID.
        """
        return self.model.obtener_paciente_por_id(id_paciente)

    def actualizar_paciente(self, id_paciente: int, datos: dict) -> bool:
        """
        Actualiza un paciente usando el modelo.
        """
        return self.model.actualizar_paciente(id_paciente, datos)

    def eliminar_paciente(self, id_paciente: int) -> bool:
        """
        Elimina un paciente usando el modelo.
        """
        return self.model.eliminar_paciente(id_paciente)
