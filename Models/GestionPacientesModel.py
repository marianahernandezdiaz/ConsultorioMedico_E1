
from Models.db_manager import DBManager


class GestionPacientesModel:
    """
    Acceso a datos para la tabla Pacientes.
    """

    def __init__(self):
        # Creamos el administrador de BD
        self.db = DBManager()

    def insertar_paciente(self, datos):
        """
        Inserta un nuevo paciente en la BD.

        datos: diccionario con claves:
            - nombres
            - apellidos
            - fecha_nac      (string 'YYYY-MM-DD' o date)
            - telefono
            - direccion
            - seguro_med

        Devuelve el ID_Paciente generado.
        """

        sql = """
            INSERT INTO Pacientes
                (Nombres, Apellidos, Fecha_nac, Telefono, Direccion, Seguro_Med)
            VALUES
                (%s, %s, %s, %s, %s, %s)
        """

        params = (
            datos["nombres"],
            datos["apellidos"],
            datos["fecha_nac"],
            datos.get("telefono"),
            datos.get("direccion"),
            datos.get("seguro_med"),
        )

        ok = self.db.execute_commit(sql, params)

        if not ok:
            # Lanzamos una excepción para que la vista pueda mostrar error
            raise Exception("No se pudo insertar el paciente en la base de datos.")

        # Usamos el cursor del DBManager para obtener el ID generado
        nuevo_id = self.db.cursor.lastrowid
        return nuevo_id

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
            # DBManager usa cursor dictionary=True, así que ya es un dict
            return resultados[0]
        return None

    def actualizar_paciente(self, id_paciente: int, datos: dict) -> bool:
        """
        Actualiza los datos de un paciente existente.
        Devuelve True si tuvo éxito, False en caso contrario.
        """
        sql = """
            UPDATE Pacientes
            SET Nombres = %s,
                Apellidos = %s,
                Fecha_nac = %s,
                Telefono = %s,
                Direccion = %s,
                Seguro_Med = %s
            WHERE ID_Paciente = %s
        """

        params = (
            datos["nombres"],
            datos["apellidos"],
            datos["fecha_nac"],
            datos.get("telefono"),
            datos.get("direccion"),
            datos.get("seguro_med"),
            id_paciente
        )

        ok = self.db.execute_commit(sql, params)
        return ok

    def eliminar_paciente(self, id_paciente: int) -> bool:
        """
        Elimina un paciente por su ID.
        Devuelve True si se eliminó alguna fila, False si no.
        """
        sql = "DELETE FROM Pacientes WHERE ID_Paciente = %s"
        params = (id_paciente,)

        ok = self.db.execute_commit(sql, params)
        return ok

    def listar_pacientes(self):
        """
        Devuelve una lista de todos los pacientes como diccionarios.
        """
        sql = """
            SELECT ID_Paciente, Nombres, Apellidos, Fecha_nac,
                    Telefono, Direccion, Seguro_Med
            FROM Pacientes
            ORDER BY ID_Paciente ASC
        """
        resultados = self.db.execute_query(sql)
        return resultados  # lista de dicts (por cursor dictionary=True)

