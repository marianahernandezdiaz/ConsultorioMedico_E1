from .db_manager import DBManager

class CitaModel:
    """Gestiona el CRUD y las consultas de la tabla Citas."""
    
    def __init__(self):
        self.db = DBManager()

    def get_citas_by_day(self, date):
        """Retorna todas las citas para un día específico."""
        query = """
        SELECT 
            C.ID_Cita, C.Fecha, C.Hora, C.Estado, C.Motivo,
            P.Nombre AS Paciente_Nombre, P.Apellidos AS Paciente_Apellido,
            U.Nombre_usuario AS Doctor_Nombre
        FROM Citas C
        JOIN Pacientes P ON C.ID_Paciente = P.ID_Paciente
        JOIN Usuarios U ON C.ID_Doctor = U.ID_Usuario
        WHERE C.Fecha = %s
        ORDER BY C.Hora
        """
        # La consulta usa JOINs para obtener los nombres completos del paciente y doctor
        return self.db.execute_query(query, (date,))
        
    def get_all_doctors(self):
        """Retorna la lista de usuarios con el rol 'Doctor'."""
        # Asumiendo que ID_Rol para Doctor es 3 (de tu script de inserción)
        query = "SELECT ID_Usuario, Nombre_usuario FROM Usuarios WHERE ID_Rol = 3"
        return self.db.execute_query(query)

    def create_cita(self, datos):
        """Agenda una nueva cita."""
        query = """
        INSERT INTO Citas (ID_Paciente, ID_Doctor, Fecha, Hora, Estado, Motivo) 
        VALUES (%s, %s, %s, %s, 'Agendada', %s)
        """
        # datos debe ser una tupla: (ID_Paciente, ID_Doctor, Fecha, Hora, Motivo)
        return self.db.execute_commit(query, datos)

    def update_cita(self, datos):
        """Modifica una cita existente."""
        # datos debe ser una tupla: (ID_Doctor, Fecha, Hora, Estado, Motivo, ID_Cita)
        query = """
        UPDATE Citas 
        SET ID_Doctor=%s, Fecha=%s, Hora=%s, Estado=%s, Motivo=%s
        WHERE ID_Cita=%s
        """
        return self.db.execute_commit(query, datos)

    def search_paciente(self, search_term):
        """Busca un paciente por nombre o apellido para agendar la cita."""
        term = f'%{search_term}%'
        query = "SELECT ID_Paciente, Nombre, Apellidos, Telefono FROM Pacientes WHERE Nombre LIKE %s OR Apellidos LIKE %s LIMIT 10"
        return self.db.execute_query(query, (term, term))