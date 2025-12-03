from .db_manager import DBManager
from config import DB_CONFIG

class UserModel:
    """
    Gestiona la interacción con las tablas Usuarios y Roles.
    """
    def __init__(self):
        # La conexión a la DB se realiza a través de DBManager
        self.db = DBManager()
        cols = self.db.execute_query("SELECT column_name AS c FROM information_schema.columns WHERE table_schema=%s AND table_name='Usuarios'", (DB_CONFIG['database'],))
        names = {r['c'] for r in cols} if cols else set()
        if 'Password' in names:
            self.pass_col = 'Password'
        elif 'Pasword' in names:
            self.pass_col = 'Pasword'
        else:
            self.pass_col = 'Contrasena'

    def get_user_by_credentials(self, email, password_hash):
        """
        Busca un usuario por email y contraseña hasheada.
        Retorna el usuario y su rol.
        """
        # Consulta para buscar al usuario y obtener su rol en una sola operación
        query = f"""
        SELECT 
            U.ID_Usuario, 
            U.Nombre_usuario, 
            R.Nombre_Rol 
        FROM Usuarios U
        JOIN Roles R ON U.ID_Rol = R.ID_Rol
        WHERE U.Email = %s AND U.{self.pass_col} = %s
        """
        # Nota: En una aplicación real, no se pasa la contraseña directamente,
        # se pasa el hash de la contraseña ingresada por el usuario.
        
        results = self.db.execute_query(query, (email, password_hash))
        
        # db.execute_query retorna una lista de diccionarios. 
        # Como el email es UNIQUE, solo esperamos un resultado (o ninguno).
        if results:
            return results[0]  # Retorna el primer y único usuario
        return None

    def close_connection(self):
        """Cierra la conexión a la DB."""
        self.db.close()
