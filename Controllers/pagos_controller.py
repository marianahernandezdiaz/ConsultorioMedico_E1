from Models.factura_model import FacturaModel

class PagosController:
    def __init__(self):
        self.model = FacturaModel()

    def list_facturas(self, estado=None):
        return self.model.list_facturas(estado)

    def set_estado(self, id_factura, estado):
        return self.model.set_estado(id_factura, estado)

    def close(self):
        self.model.close()
