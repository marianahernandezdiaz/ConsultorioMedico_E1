from .db_manager import DBManager

class CitaModel:
    """Gestiona el CRUD, consultas y validación de la tabla Citas."""
    
    def __init__(self):
        self.db = DBManager()
        
    def get_all_doctors(self):
        """Retorna la lista de usuarios con el rol 'Doctor' (ID_Rol = 3)."""
        query = "SELECT ID_Usuario, Nombre_usuario FROM Usuarios WHERE ID_Rol = 3"
        return self.db.execute_query(query)

    def obtener_paciente_por_id(self, id_paciente: int):
        """
        Devuelve un paciente como diccionario (o None si no existe)
        """
        sql = """
            SELECT ID_Paciente, Nombres, Apellidos, Fecha_nac,
                Telefono, Direccion, Seguro_Med
            FROM Pacientes
            WHERE ID_Paciente = %s
        """
        params = (id_paciente,)

        resultados = self.db.execute_query(sql, params)
        if resultados:
            return resultados[0]
        return None


    def get_citas_by_day(self, date):
        """Retorna todas las citas para un día específico."""
        query = """
        SELECT 
            C.ID_Cita, C.Fecha, C.Hora, C.Estado, C.Motivo,
            P.Nombres AS Paciente_Nombre, P.Apellidos AS Paciente_Apellido,
            U.Nombre_usuario AS Doctor_Nombre
        FROM citas C
        JOIN pacientes P ON C.ID_Paciente = P.ID_Paciente
        JOIN Usuarios U ON C.ID_Doctor = U.ID_Usuario
        WHERE C.Fecha = %s
        ORDER BY C.Hora
        """
        return self.db.execute_query(query, (date,))

    def get_cita_details(self, cita_id):
        """Retorna todos los detalles de una cita por su ID (fuente de la precarga)."""
        query = """
        SELECT 
            C.ID_Cita,
            C.ID_Paciente AS ID_Paciente, 
            C.ID_Doctor,
            C.Fecha, 
            C.Hora, 
            C.Estado, 
            C.Motivo,
            P.Nombres AS Paciente_Nombre, 
            P.Apellidos AS Paciente_Apellido,
            U.ID_Usuario AS Doctor_ID, 
            U.Nombre_usuario AS Doctor_Nombre
        FROM citas C
        JOIN Pacientes P ON C.ID_Paciente = P.ID_Paciente
        JOIN Usuarios U ON C.ID_Doctor = U.ID_Usuario
        WHERE C.ID_Cita = %s
        """
        result = self.db.execute_query(query, (cita_id,))
        return result[0] if result else None

    def create_cita(self, paciente_id, doctor_id, fecha, hora, motivo):
        """Agenda una nueva cita (DML)."""
        query = """
        INSERT INTO citas (ID_Paciente, ID_Doctor, Fecha, Hora, Estado, Motivo) 
        VALUES (%s, %s, %s, %s, 'Agendada', %s)
        """
        datos = (paciente_id, doctor_id, fecha, hora, motivo)
        return self.db.execute_dml(query, datos)

    def update_cita(self, cita_id, id_doctor, fecha, hora, motivo, estado):
       
        cita_id_int = int(cita_id) 
        id_doctor_int = int(id_doctor) # Asegurar el tipo
        query = """
        UPDATE citas 
        SET ID_Doctor = %s, Fecha = %s, Hora = %s, Motivo = %s, Estado = %s
        WHERE ID_Cita = %s;
        """
        params = (id_doctor_int, fecha, hora, motivo, estado, cita_id_int)
        
        # Llama al ejecutor DML
        return self.db.execute_dml(query, params)


    def check_cita_conflict(self, id_cita_to_exclude, id_doctor, fecha, hora):
        """Verifica si ya existe una cita para un doctor en ese horario."""
        query = """
        SELECT COUNT(*) 
        FROM citas 
        WHERE ID_Doctor = %s AND Fecha = %s AND Hora = %s AND ID_Cita != %s;
        """
        params = (id_doctor, fecha, hora, id_cita_to_exclude)
        result = self.db.execute_query(query, params)
        
        if result and result[0]:
            # El resultado es [{ 'COUNT(*)': 1 }]
            conflict_count = result[0]['COUNT(*)']
            return conflict_count > 0
        else:
            return False
        
        
        
    