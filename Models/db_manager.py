import mysql.connector
from config import DB_CONFIG # Importamos la configuración
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
        
        try:
            # Intenta establecer la conexión usando las credenciales de config.py
            self.connection = mysql.connector.connect(**DB_CONFIG)
            
            # Verifica si la conexión fue exitosa
            if self.connection.is_connected():
                print(f"✅ Conexión a la base de datos '{DB_CONFIG['database']}' exitosa.")
                self.cursor = self.connection.cursor(dictionary=True) 

            else:
                print("No se pudo conectar a la base de datos.")

        except mysql.connector.Error as err:
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
            
        except mysql.connector.Error as err:
            print(f"Error fatal al intentar crear la base de datos: {err}")
            print("Por favor, verifica tus permisos de usuario o crea la base de datos manualmente.")


    def close(self):
        """
        Cierra el cursor y la conexión a la base de datos.
        """
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔌 Conexión a MySQL cerrada.")
            
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
            except mysql.connector.Error as err:
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
            except mysql.connector.Error as err:
                # Si hay un error, haz ROLLBACK
                self.connection.rollback()
                print(f"Error al ejecutar COMMIT ({query}): {err}")
                return False
        return False
