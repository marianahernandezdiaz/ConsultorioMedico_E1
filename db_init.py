# import mysql.connector
# from config import DB_CONFIG

# cfg = DB_CONFIG.copy()
# db_name = cfg['database']

# temp_cfg = cfg.copy()
# temp_cfg.pop('database', None)

# conn = mysql.connector.connect(**temp_cfg)
# cur = conn.cursor()
# cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
# cur.close()
# conn.close()

# conn = mysql.connector.connect(**cfg)
# cur = conn.cursor()

# statements = [
#     """
#     CREATE TABLE IF NOT EXISTS Roles (
#         ID_Rol INT PRIMARY KEY AUTO_INCREMENT,
#         Nombre_Rol VARCHAR(50) NOT NULL UNIQUE
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Usuarios (
#         ID_Usuario INT PRIMARY KEY AUTO_INCREMENT,
#         ID_Rol INT NOT NULL,
#         Nombre_usuario VARCHAR(100) NOT NULL,
#         Email VARCHAR(100) NOT NULL UNIQUE,
#         Contrasena VARCHAR(255) NOT NULL,
#         FOREIGN KEY (ID_Rol) REFERENCES Roles(ID_Rol)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Pacientes (
#         ID_Paciente INT PRIMARY KEY AUTO_INCREMENT,
#         Nombres VARCHAR(100) NOT NULL,
#         Apellidos VARCHAR(100) NOT NULL,
#         Fecha_nac DATE NOT NULL,
#         Telefono VARCHAR(20),
#         Direccion VARCHAR(100),
#         Seguro_Med VARCHAR(100)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Citas (
#         ID_Cita INT PRIMARY KEY AUTO_INCREMENT,
#         ID_Paciente INT NOT NULL,
#         ID_Doctor INT NOT NULL,
#         Fecha DATE NOT NULL,
#         Hora TIME NOT NULL,
#         Estado VARCHAR(50) NOT NULL DEFAULT 'Agendada',
#         Motivo VARCHAR(255),
#         UNIQUE KEY (ID_Doctor, Fecha, Hora),
#         FOREIGN KEY (ID_Paciente) REFERENCES Pacientes(ID_Paciente),
#         FOREIGN KEY (ID_Doctor) REFERENCES Usuarios(ID_Usuario)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Historial_Medico (
#         ID_Historial INT PRIMARY KEY AUTO_INCREMENT,
#         ID_Cita INT NOT NULL,
#         Diagnostico TEXT NOT NULL,
#         Tratamiento TEXT NOT NULL,
#         Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
#         ID_Doctor INT NOT NULL,
#         FOREIGN KEY (ID_Cita) REFERENCES Citas(ID_Cita),
#         FOREIGN KEY (ID_Doctor) REFERENCES Usuarios(ID_Usuario)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Servicios (
#         ID_Servicio INT PRIMARY KEY AUTO_INCREMENT,
#         Nombre_Servicio VARCHAR(100) NOT NULL UNIQUE,
#         Costo DECIMAL(10, 2) NOT NULL CHECK (Costo >= 0)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Facturas (
#         ID_Factura INT PRIMARY KEY AUTO_INCREMENT,
#         ID_Cita INT,
#         Fecha_Emision DATE NOT NULL,
#         Total DECIMAL(10, 2) NOT NULL CHECK (Total >= 0),
#         Estado_Pago VARCHAR(50) NOT NULL,
#         ID_Paciente INT NOT NULL,
#         FOREIGN KEY (ID_Cita) REFERENCES Citas(ID_Cita),
#         FOREIGN KEY (ID_Paciente) REFERENCES Pacientes(ID_Paciente)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
#     """
#     CREATE TABLE IF NOT EXISTS Detalle_Factura (
#         ID_Detalle INT PRIMARY KEY AUTO_INCREMENT,
#         ID_Factura INT NOT NULL,
#         ID_Servicio INT NOT NULL,
#         Cantidad INT NOT NULL DEFAULT 1 CHECK (Cantidad >= 1),
#         Precio_Unitario DECIMAL(10, 2) NOT NULL,
#         FOREIGN KEY (ID_Factura) REFERENCES Facturas(ID_Factura),
#         FOREIGN KEY (ID_Servicio) REFERENCES Servicios(ID_Servicio)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#     """,
# ]

# for s in statements:
#     cur.execute(s)

# cur.execute(
#     """
#     INSERT IGNORE INTO Roles (Nombre_Rol) VALUES
#     ('Administrador'),
#     ('Recepcionista'),
#     ('Doctor')
#     """
# )

# cur.execute(
#     """
#     INSERT IGNORE INTO Usuarios (ID_Rol, Nombre_usuario, Email, Contrasena) VALUES
#     (1, 'Admin Principal', 'admin@clinica.com', '123'),
#     (2, 'Laura Recepcionista', 'recepcionista@clinica.com', '456'),
#     (3, 'Dr. Hernandez', 'doctor@clinica.com', '789')
#     """
# )

# conn.commit()

# cur.execute("SELECT COUNT(*) FROM Roles")
# roles_count = cur.fetchone()[0]
# cur.execute("SELECT COUNT(*) FROM Usuarios")
# users_count = cur.fetchone()[0]
# print(f"roles={roles_count} usuarios={users_count}")

# # --- Seed de servicios ---
# cur.execute("SELECT COUNT(*) FROM Servicios")
# svc_count = cur.fetchone()[0]
# if svc_count == 0:
#     cur.execute(
#         """
#         INSERT IGNORE INTO Servicios (Nombre_Servicio, Costo) VALUES
#         ('Consulta general', 300.00),
#         ('Ultrasonido', 900.00),
#         ('Radiografía', 450.00),
#         ('Vacunación', 250.00),
#         ('Análisis de laboratorio', 700.00)
#         """
#     )

# # --- Seed de pacientes ---
# cur.execute("SELECT COUNT(*) FROM Pacientes")
# pac_count = cur.fetchone()[0]
# if pac_count == 0:
#     cur.execute(
#         """
#         INSERT INTO Pacientes (Nombres, Apellidos, Fecha_nac, Telefono, Direccion, Seguro_Med) VALUES
#         ('Ana María', 'Lopez Perez', '1990-05-12', '555-1111', 'Calle 1 #123', 'Seguro A'),
#         ('Carlos', 'Gomez Ruiz', '1985-03-22', '555-2222', 'Calle 2 #456', 'Seguro B'),
#         ('Luisa', 'Fernandez Díaz', '1992-11-03', '555-3333', 'Av. Central 78', 'Seguro A'),
#         ('Miguel', 'Santos Lara', '1978-07-19', '555-4444', 'Av. Norte 13', 'Seguro C'),
#         ('Daniela', 'Ramírez Soto', '2001-02-15', '555-5555', 'Col. Sur 5', 'Seguro B'),
#         ('Jorge', 'Hernández Cruz', '1995-09-09', '555-6666', 'Calle Lago 20', 'Seguro A'),
#         ('María', 'Martínez Vega', '1988-12-30', '555-7777', 'Av. Bosque 10', 'Seguro C'),
#         ('Sofía', 'Núñez Ríos', '1999-08-25', '555-8888', 'Col. Centro 3', 'Seguro B')
#         """
#     )

# # --- Seed de citas, historial y facturación ---
# cur.execute("SELECT COUNT(*) FROM Citas")
# cit_count = cur.fetchone()[0]
# if cit_count == 0:
#     # Obtener IDs necesarios
#     cur.execute("SELECT ID_Usuario FROM Usuarios WHERE ID_Rol = (SELECT ID_Rol FROM Roles WHERE Nombre_Rol='Doctor') LIMIT 1")
#     row = cur.fetchone()
#     doctor_id = row[0] if row else 3
#     cur.execute("SELECT ID_Paciente FROM Pacientes ORDER BY ID_Paciente")
#     pacientes = [r[0] for r in cur.fetchall()]

#     # Fechas y horas fijas para reproducibilidad
#     from datetime import date, timedelta
#     base = date.today()
#     horas = ["09:00:00", "11:00:00", "15:00:00"]

#     created_citas = []
#     for d in range(0, 12):
#         fecha = base - timedelta(days=d)
#         for h_idx, h in enumerate(horas):
#             pac_id = pacientes[(d*len(horas)+h_idx) % len(pacientes)]
#             cur.execute(
#                 """
#                 INSERT INTO Citas (ID_Paciente, ID_Doctor, Fecha, Hora, Estado, Motivo)
#                 VALUES (%s, %s, %s, %s, 'Agendada', 'Consulta')
#                 """,
#                 (pac_id, doctor_id, fecha, h)
#             )
#             created_citas.append(cur.lastrowid)

#     # Marcar aproximadamente 60% como completadas en Historial_Medico
#     completadas = created_citas[::2] + created_citas[3::5]
#     for cid in completadas:
#         cur.execute(
#             """
#             INSERT INTO Historial_Medico (ID_Cita, Diagnostico, Tratamiento, ID_Doctor)
#             VALUES (%s, 'Diagnóstico estándar', 'Reposo y medicación', %s)
#             """,
#             (cid, doctor_id)
#         )

#     # Crear facturas para las completadas
#     # Obtener mapa de servicios y costos
#     cur.execute("SELECT ID_Servicio, Costo FROM Servicios")
#     svc_rows = cur.fetchall()
#     if svc_rows:
#         svc_ids = [r[0] for r in svc_rows]
#         svc_cost = {r[0]: r[1] for r in svc_rows}
#         for idx, cid in enumerate(completadas):
#             # Encontrar paciente de la cita
#             cur.execute("SELECT ID_Paciente, Fecha FROM Citas WHERE ID_Cita=%s", (cid,))
#             p_row = cur.fetchone()
#             if not p_row:
#                 continue
#             pid, f_emision = p_row[0], p_row[1]
#             estado = 'Pagado' if idx % 2 == 0 else 'Pendiente'
#             total = 0.0
#             cur.execute(
#                 """
#                 INSERT INTO Facturas (ID_Cita, Fecha_Emision, Total, Estado_Pago, ID_Paciente)
#                 VALUES (%s, %s, %s, %s, %s)
#                 """,
#                 (cid, f_emision, 0.0, estado, pid)
#             )
#             fid = cur.lastrowid
#             # Agregar 1-2 servicios
#             import random
#             count = 1 + (idx % 2)
#             chosen = random.sample(svc_ids, k=count)
#             for sid in chosen:
#                 price = float(svc_cost[sid])
#                 total += price
#                 cur.execute(
#                     """
#                     INSERT INTO Detalle_Factura (ID_Factura, ID_Servicio, Cantidad, Precio_Unitario)
#                     VALUES (%s, %s, 1, %s)
#                     """,
#                     (fid, sid, price)
#                 )
#             # Actualizar total
#             cur.execute("UPDATE Facturas SET Total=%s WHERE ID_Factura=%s", (round(total,2), fid))

# conn.commit()

# # Resumen
# cur.execute("SELECT COUNT(*) FROM Pacientes")
# pacientes_total = cur.fetchone()[0]
# cur.execute("SELECT COUNT(*) FROM Citas")
# citas_total = cur.fetchone()[0]
# cur.execute("SELECT COUNT(*) FROM Historial_Medico")
# hist_total = cur.fetchone()[0]
# cur.execute("SELECT COUNT(*) FROM Facturas")
# fac_total = cur.fetchone()[0]
# cur.execute("SELECT COUNT(*) FROM Detalle_Factura")
# det_total = cur.fetchone()[0]
# print(f"pacientes={pacientes_total} citas={citas_total} historial={hist_total} facturas={fac_total} detalles={det_total}")

# cur.close()
# conn.close()