from .db_manager import DBManager

class FacturaModel:
    def __init__(self):
        self.db = DBManager()

    def create_factura(self, id_cita, id_paciente, fecha_emision, total, estado_pago):
        q = (
            "INSERT INTO Facturas (ID_Cita, Fecha_Emision, Total, Estado_Pago, ID_Paciente) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        ok = self.db.execute_commit(q, (id_cita, fecha_emision, total, estado_pago, id_paciente))
        if not ok:
            return None
        res = self.db.execute_query("SELECT LAST_INSERT_ID() AS id")
        return res[0]["id"] if res else None

    def add_detalle(self, id_factura, id_servicio, cantidad, precio_unitario):
        q = (
            "INSERT INTO Detalle_Factura (ID_Factura, ID_Servicio, Cantidad, Precio_Unitario) "
            "VALUES (%s, %s, %s, %s)"
        )
        return self.db.execute_commit(q, (id_factura, id_servicio, cantidad, precio_unitario))

    def list_facturas(self, estado=None):
        if estado:
            return self.db.execute_query("SELECT * FROM Facturas WHERE Estado_Pago=%s ORDER BY ID_Factura DESC", (estado,))
        return self.db.execute_query("SELECT * FROM Facturas ORDER BY ID_Factura DESC")

    def set_estado(self, id_factura, estado):
        return self.db.execute_commit("UPDATE Facturas SET Estado_Pago=%s WHERE ID_Factura=%s", (estado, id_factura))

    def close(self):
        self.db.close()

    def get_or_create_servicio(self, nombre, costo):
        r = self.db.execute_query("SELECT ID_Servicio FROM Servicios WHERE Nombre_Servicio=%s", (nombre,))
        if r:
            return r[0]["ID_Servicio"]
        ok = self.db.execute_commit("INSERT INTO Servicios (Nombre_Servicio, Costo) VALUES (%s, %s)", (nombre, costo))
        if not ok:
            return None
        res = self.db.execute_query("SELECT LAST_INSERT_ID() AS id")
        return res[0]["id"] if res else None

    def paciente_exists(self, pid):
        r = self.db.execute_query("SELECT 1 FROM Pacientes WHERE ID_Paciente=%s", (pid,))
        return bool(r)

    def cita_exists(self, cid):
        r = self.db.execute_query("SELECT 1 FROM Citas WHERE ID_Cita=%s", (cid,))
        return bool(r)

    def create_demo_paciente(self):
        ok = self.db.execute_commit(
            "INSERT INTO Pacientes (Nombres, Apellidos, Fecha_nac, Telefono, Direccion, Seguro_Med) VALUES (%s,%s,%s,%s,%s,%s)",
            ("Paciente", "Demo", "1990-01-01", None, None, None),
        )
        if not ok:
            return None
        res = self.db.execute_query("SELECT LAST_INSERT_ID() AS id")
        return res[0]["id"] if res else None
