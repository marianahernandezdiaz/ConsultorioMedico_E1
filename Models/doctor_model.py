from .db_manager import DBManager

class DoctorModel:
    def __init__(self):
        self.db = DBManager()

    def get_todos_pacientes(self):
        query = "SELECT ID_Paciente, Nombres, Apellidos, Telefono FROM Pacientes"
        return self.db.execute_query(query)

    def get_historial_medico(self, id_paciente):
        """
        CORRECCIÓN: Ahora traemos también ID_Historial para poder editar/eliminar.
        """
        query = """
            SELECT h.ID_Historial, h.Fecha_Registro, h.Diagnostico, h.Tratamiento, u.Nombre_usuario as Doctor
            FROM Historial_Medico h
            JOIN Usuarios u ON h.ID_Doctor = u.ID_Usuario
            JOIN Citas c ON h.ID_Cita = c.ID_Cita
            WHERE c.ID_Paciente = %s
            ORDER BY h.Fecha_Registro DESC
        """
        return self.db.execute_query(query, (id_paciente,))

    def get_ultima_cita_id(self, id_paciente):
        query = """
            SELECT ID_Cita FROM Citas 
            WHERE ID_Paciente = %s 
            ORDER BY Fecha DESC, Hora DESC 
            LIMIT 1
        """
        result = self.db.execute_query(query, (id_paciente,))
        return result[0]['ID_Cita'] if result else None

    # --- CRUD: CREATE ---
    def guardar_consulta(self, id_cita, diagnostico, tratamiento, id_doctor):
        try:
            query_insert = """
                INSERT INTO Historial_Medico (ID_Cita, Diagnostico, Tratamiento, ID_Doctor) 
                VALUES (%s, %s, %s, %s)
            """

            self.db.execute_commit("UPDATE Citas SET Estado = 'Atendida' WHERE ID_Cita = %s", (id_cita,))
            return self.db.execute_commit(query_insert, (id_cita, diagnostico, tratamiento, id_doctor))
        except Exception as e:
            print(f"Error create: {e}")
            return False

    # --- CRUD: UPDATE ---
    def actualizar_historial(self, id_historial, diagnostico, tratamiento):
        query = """
            UPDATE Historial_Medico 
            SET Diagnostico = %s, Tratamiento = %s 
            WHERE ID_Historial = %s
        """
        return self.db.execute_commit(query, (diagnostico, tratamiento, id_historial))

    # --- CRUD: DELETE ---
    def eliminar_historial(self, id_historial):
        query = "DELETE FROM Historial_Medico WHERE ID_Historial = %s"
        return self.db.execute_commit(query, (id_historial,))
        
    def close_connection(self):
        self.db.close()