from Models.factura_model import FacturaModel

class FacturacionController:
    def __init__(self):
        self.model = FacturaModel()

    def paciente_exists(self, pid):
        return self.model.paciente_exists(pid)

    def cita_exists(self, cid):
        return self.model.cita_exists(cid)

    def create_demo_paciente(self):
        return self.model.create_demo_paciente()

    def get_or_create_servicio(self, nombre, costo):
        return self.model.get_or_create_servicio(nombre, costo)

    def create_factura(self, id_cita, id_paciente, fecha_emision, total, estado_pago):
        return self.model.create_factura(id_cita, id_paciente, fecha_emision, total, estado_pago)

    def add_detalle(self, id_factura, id_servicio, cantidad, precio_unitario):
        return self.model.add_detalle(id_factura, id_servicio, cantidad, precio_unitario)

    def close(self):
        self.model.close()
