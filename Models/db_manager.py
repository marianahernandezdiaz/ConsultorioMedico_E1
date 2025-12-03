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
                try:
                    self.init_schema()
                except Exception as _:
                    pass
                try:
                    self.seed_demo_data()
                except Exception as _:
                    pass

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

    def init_schema(self):
        if not (self.connection and self.connection.is_connected()):
            return False
        statements = [
            "CREATE TABLE IF NOT EXISTS Roles (ID_Rol INT PRIMARY KEY AUTO_INCREMENT, Nombre_Rol VARCHAR(50) NOT NULL UNIQUE)",
            "CREATE TABLE IF NOT EXISTS Usuarios (ID_Usuario INT PRIMARY KEY AUTO_INCREMENT, ID_Rol INT NOT NULL, Nombre_usuario VARCHAR(100) NOT NULL, Email VARCHAR(100) NOT NULL UNIQUE, Contrasena VARCHAR(255) NOT NULL, FOREIGN KEY (ID_Rol) REFERENCES Roles(ID_Rol))",
            "CREATE TABLE IF NOT EXISTS Pacientes (ID_Paciente INT PRIMARY KEY AUTO_INCREMENT, Nombres VARCHAR(100) NOT NULL, Apellidos VARCHAR(100) NOT NULL, Fecha_nac DATE NOT NULL, Telefono VARCHAR(20), Direccion VARCHAR(100), Seguro_Med VARCHAR(100))",
            "CREATE TABLE IF NOT EXISTS Citas (ID_Cita INT PRIMARY KEY AUTO_INCREMENT, ID_Paciente INT NOT NULL, ID_Doctor INT NOT NULL, Fecha DATE NOT NULL, Hora TIME NOT NULL, Estado VARCHAR(50) NOT NULL DEFAULT 'Agendada', Motivo VARCHAR(255), UNIQUE KEY uq_doctor_fecha_hora (ID_Doctor, Fecha, Hora), FOREIGN KEY (ID_Paciente) REFERENCES Pacientes(ID_Paciente), FOREIGN KEY (ID_Doctor) REFERENCES Usuarios(ID_Usuario))",
            "CREATE TABLE IF NOT EXISTS Historial_Medico (ID_Historial INT PRIMARY KEY AUTO_INCREMENT, ID_Cita INT NOT NULL, Diagnostico TEXT NOT NULL, Tratamiento TEXT NOT NULL, Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP, ID_Doctor INT NOT NULL, FOREIGN KEY (ID_Cita) REFERENCES Citas(ID_Cita), FOREIGN KEY (ID_Doctor) REFERENCES Usuarios(ID_Usuario))",
            "CREATE TABLE IF NOT EXISTS Servicios (ID_Servicio INT PRIMARY KEY AUTO_INCREMENT, Nombre_Servicio VARCHAR(100) NOT NULL UNIQUE, Costo DECIMAL(10, 2) NOT NULL)",
            "CREATE TABLE IF NOT EXISTS Facturas (ID_Factura INT PRIMARY KEY AUTO_INCREMENT, ID_Cita INT, Fecha_Emision DATE NOT NULL, Total DECIMAL(10, 2) NOT NULL, Estado_Pago VARCHAR(50) NOT NULL, ID_Paciente INT NOT NULL, FOREIGN KEY (ID_Cita) REFERENCES Citas(ID_Cita), FOREIGN KEY (ID_Paciente) REFERENCES Pacientes(ID_Paciente))",
            "CREATE TABLE IF NOT EXISTS Detalle_Factura (ID_Detalle INT PRIMARY KEY AUTO_INCREMENT, ID_Factura INT NOT NULL, ID_Servicio INT NOT NULL, Cantidad INT NOT NULL DEFAULT 1, Precio_Unitario DECIMAL(10, 2) NOT NULL, FOREIGN KEY (ID_Factura) REFERENCES Facturas(ID_Factura), FOREIGN KEY (ID_Servicio) REFERENCES Servicios(ID_Servicio))",
            "INSERT IGNORE INTO Roles (Nombre_Rol) VALUES ('Administrador'), ('Recepcionista'), ('Doctor')"
        ]
        try:
            for s in statements:
                self.cursor.execute(s)
                self.connection.commit()
            pass_col = "Contrasena"
            check = self.execute_query("SELECT 1 FROM information_schema.columns WHERE table_schema=%s AND table_name='Usuarios' AND column_name='Contrasena'", (DB_CONFIG['database'],))
            if not check:
                self.cursor.execute("ALTER TABLE Usuarios ADD COLUMN Pasword VARCHAR(255) NOT NULL")
                self.connection.commit()
                pass_col = "Pasword"
            else:
                check2 = self.execute_query("SELECT 1 FROM information_schema.columns WHERE table_schema=%s AND table_name='Usuarios' AND column_name='Pasword'", (DB_CONFIG['database'],))
                if check2:
                    pass_col = "Pasword"
            self.cursor.execute(f"INSERT IGNORE INTO Usuarios (ID_Rol, Nombre_usuario, Email, {pass_col}) VALUES (1, 'Admin Principal', 'admin@clinica.com', '123'), (2, 'Laura Recepcionista', 'recepcionista@clinica.com', '456'), (3, 'Dr. Hernandez', 'doctor@clinica.com', '789')")
            self.connection.commit()
            return True
        except Exception as err:
            print(f"Error al inicializar esquema: {err}")
            return False

    def seed_demo_data(self):
        cnt_serv = self.execute_query("SELECT COUNT(*) AS c FROM Servicios")
        if cnt_serv and cnt_serv[0]["c"] == 0:
            self.execute_commit("INSERT INTO Servicios (Nombre_Servicio, Costo) VALUES (%s,%s)", ("Consulta General", 300.0))
            self.execute_commit("INSERT INTO Servicios (Nombre_Servicio, Costo) VALUES (%s,%s)", ("Rayos X", 500.0))
            self.execute_commit("INSERT INTO Servicios (Nombre_Servicio, Costo) VALUES (%s,%s)", ("Laboratorio", 250.0))

        cnt_pac = self.execute_query("SELECT COUNT(*) AS c FROM Pacientes")
        if cnt_pac and cnt_pac[0]["c"] == 0:
            name_col = "Nombres"
            if not self.execute_query("SELECT 1 FROM information_schema.columns WHERE table_schema=%s AND table_name='Pacientes' AND column_name='Nombres'", (DB_CONFIG['database'],)):
                name_col = "Nombre(s)"
            q = f"INSERT INTO Pacientes (`{name_col}`, `Apellidos`, `Fecha_nac`, `Telefono`, `Direccion`, `Seguro_Med`) VALUES (%s,%s,%s,%s,%s,%s)"
            self.execute_commit(q, ("Juan", "Pérez", "1988-03-15", "555-1234", "Calle 1", "Seguro A"))
            self.execute_commit(q, ("Ana", "López", "1992-07-21", "555-5678", "Calle 2", "Seguro B"))

        cnt_cita = self.execute_query("SELECT COUNT(*) AS c FROM Citas")
        if cnt_cita and cnt_cita[0]["c"] == 0:
            self.execute_commit(
                "INSERT INTO Citas (ID_Paciente, ID_Doctor, Fecha, Hora, Estado, Motivo) VALUES (%s,%s,%s,%s,%s,%s)",
                (1, 3, "2025-11-25", "09:00:00", "Agendada", "Consulta de prueba"),
            )
