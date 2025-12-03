CREATE DATABASE IF NOT EXISTS consultorio_medico;
USE consultorio_medico;

CREATE TABLE IF NOT EXISTS Roles (
  ID_Rol INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Rol VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Usuarios (
  ID_Usuario INT PRIMARY KEY AUTO_INCREMENT,
  ID_Rol INT NOT NULL,
  Nombre_usuario VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL UNIQUE,
  Password VARCHAR(255) NOT NULL,
  FOREIGN KEY (ID_Rol) REFERENCES Roles(ID_Rol)
);

CREATE TABLE IF NOT EXISTS Pacientes (
  ID_Paciente INT PRIMARY KEY AUTO_INCREMENT,
  Nombres VARCHAR(100) NOT NULL,
  Apellidos VARCHAR(100) NOT NULL,
  Fecha_nac DATE NOT NULL,
  Telefono VARCHAR(20),
  Direccion VARCHAR(100),
  Seguro_Med VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Citas (
  ID_Cita INT PRIMARY KEY AUTO_INCREMENT,
  ID_Paciente INT NOT NULL,
  ID_Doctor INT NOT NULL,
  Fecha DATE NOT NULL,
  Hora TIME NOT NULL,
  Estado VARCHAR(50) NOT NULL DEFAULT 'Agendada',
  Motivo VARCHAR(255),
  UNIQUE KEY uq_doctor_fecha_hora (ID_Doctor, Fecha, Hora),
  FOREIGN KEY (ID_Paciente) REFERENCES Pacientes(ID_Paciente),
  FOREIGN KEY (ID_Doctor) REFERENCES Usuarios(ID_Usuario)
);

CREATE TABLE IF NOT EXISTS Historial_Medico (
  ID_Historial INT PRIMARY KEY AUTO_INCREMENT,
  ID_Cita INT NOT NULL,
  Diagnostico TEXT NOT NULL,
  Tratamiento TEXT NOT NULL,
  Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  ID_Doctor INT NOT NULL,
  FOREIGN KEY (ID_Cita) REFERENCES Citas(ID_Cita),
  FOREIGN KEY (ID_Doctor) REFERENCES Usuarios(ID_Usuario)
);

CREATE TABLE IF NOT EXISTS Servicios (
  ID_Servicio INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Servicio VARCHAR(100) NOT NULL UNIQUE,
  Costo DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Facturas (
  ID_Factura INT PRIMARY KEY AUTO_INCREMENT,
  ID_Cita INT,
  Fecha_Emision DATE NOT NULL,
  Total DECIMAL(10,2) NOT NULL,
  Estado_Pago VARCHAR(50) NOT NULL,
  ID_Paciente INT NOT NULL,
  FOREIGN KEY (ID_Cita) REFERENCES Citas(ID_Cita),
  FOREIGN KEY (ID_Paciente) REFERENCES Pacientes(ID_Paciente)
);

CREATE TABLE IF NOT EXISTS Detalle_Factura (
  ID_Detalle INT PRIMARY KEY AUTO_INCREMENT,
  ID_Factura INT NOT NULL,
  ID_Servicio INT NOT NULL,
  Cantidad INT NOT NULL DEFAULT 1,
  Precio_Unitario DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (ID_Factura) REFERENCES Facturas(ID_Factura),
  FOREIGN KEY (ID_Servicio) REFERENCES Servicios(ID_Servicio)
);

INSERT INTO Roles (Nombre_Rol) VALUES ('Administrador'), ('Recepcionista'), ('Doctor');

INSERT INTO Usuarios (ID_Rol, Nombre_usuario, Email, Password) VALUES
  (1, 'Admin Principal', 'admin@clinica.com', '123'),
  (2, 'Laura Recepcionista', 'recepcionista@clinica.com', '456'),
  (3, 'Dr. Hernandez', 'doctor@clinica.com', '789');

INSERT INTO Pacientes (Nombres, Apellidos, Fecha_nac, Telefono, Direccion, Seguro_Med) VALUES
  ('Juan', 'Perez', '1990-05-15', '555-1234', 'Calle 1', 'GNP'),
  ('Maria', 'Lopez', '1985-08-20', '555-5678', 'Calle 2', 'AXA');

INSERT INTO Citas (ID_Paciente, ID_Doctor, Fecha, Hora, Motivo) VALUES
  (1, 3, CURDATE(), '10:00:00', 'Dolor de cabeza recurrente');
