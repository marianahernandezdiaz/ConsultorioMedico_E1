try:
    import mysql.connector
except Exception:
    mysql = None
from config import DB_CONFIG
## Clase para gestionar la conexión a la base de datos MySQL
class DBManager:
    """
    Clase para gestionar la conexión a la base de datos MySQL.
    """
    
    def __init__(self):
        """
        Inicializa la conexión a la base de datos.
        """
        self.connection = None
        self.cursor = None
        
        if mysql is None:
            print("Conector MySQL no disponible. Instale mysql-connector-python.")
            return
        try:
            # Intenta establecer la conexión usando las credenciales de config.py
            self.connection = mysql.connector.connect(**DB_CONFIG)
            
            # Verifica si la conexión fue exitosa
            if self.connection.is_connected():
                print(f"Conexión a la base de datos '{DB_CONFIG['database']}' exitosa.")
                self.cursor = self.connection.cursor(dictionary=True)

            else:
                print("No se pudo conectar a la base de datos.")

        except Exception as err:
            print(f"Error al conectar a MySQL: {err}")
            if err.errno == 1049:
                self._create_database()
            
    def _create_database(self):
        """
        Intenta crear la base de datos si no existe.
        """
        print("La base de datos no existe. Intentando crearla...")
        
        # Intentamos conectar sin especificar la base de datos
        temp_config = DB_CONFIG.copy()
        db_name = temp_config.pop('database')
        
        if mysql is None:
            print("Conector MySQL no disponible. No se puede crear la base de datos.")
            return
        try:
            temp_conn = mysql.connector.connect(**temp_config)
            temp_cursor = temp_conn.cursor()
            
            # Ejecutamos el comando para crear la base de datos
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Base de datos '{db_name}' creada exitosamente.")
            
            # Cerramos la conexión temporal y volvemos a intentar la conexión principal
            temp_cursor.close()
            temp_conn.close()
            
            self.__init__() # Reintentar la conexión completa
            
        except Exception as err:
            print(f"Error fatal al intentar crear la base de datos: {err}")
            print("Por favor, verifica tus permisos de usuario o crea la base de datos manualmente.")


    def close(self):
        """
        Cierra el cursor y la conexión a la base de datos.
        """
        if self.connection and self.connection.is_connected():
            try:
                if self.cursor:
                    self.cursor.close()
            except Exception:
                pass
            try:
                self.connection.close()
            except Exception:
                pass
            print("Conexión a MySQL cerrada.")
            
    # --- Métodos de Utilidad para Ejecutar Consultas ---
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL de SELECT.
        Retorna los resultados o una lista vacía.
        """
        if self.connection and self.connection.is_connected():
            try:
                self.cursor.execute(query, params)
                return self.cursor.fetchall()
            except Exception as err:
                print(f"Error al ejecutar SELECT: {err}")
                return []
        return []

    def execute_commit(self, query, params=None):
        """
        Ejecuta una consulta SQL de INSERT, UPDATE o DELETE y aplica el COMMIT.
        Retorna True en caso de éxito, False en caso de error.
        """
        if self.connection and self.connection.is_connected():
            try:
                self.cursor.execute(query, params)
                self.connection.commit()
                return True
            except Exception as err:
                self.connection.rollback()
                print(f"Error al ejecutar COMMIT ({query}): {err}")
                return False
        return False

    

        cnt_cita = self.execute_query("SELECT COUNT(*) AS c FROM Citas")
        if cnt_cita and cnt_cita[0]["c"] == 0:
            self.execute_commit(
                "INSERT INTO Citas (ID_Paciente, ID_Doctor, Fecha, Hora, Estado, Motivo) VALUES (%s,%s,%s,%s,%s,%s)",
                (1, 3, "2025-11-25", "09:00:00", "Agendada", "Consulta de prueba"),
            )
