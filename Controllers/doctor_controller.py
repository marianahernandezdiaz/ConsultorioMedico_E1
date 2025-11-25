from tkinter import messagebox
from Models.doctor_model import DoctorModel
from Views.doctor_view import DoctorView

class DoctorController:
    def __init__(self, root, user_data):
        self.root = root
        self.doctor_id = user_data['ID_Usuario']
        
        self.model = DoctorModel()
        self.view = DoctorView(self.root, self, user_data['Nombre_usuario'])
        
        self.paciente_seleccionado_id = None
        self.registro_seleccionado_id = None # ID del Historial seleccionado para editar/eliminar
        
        self.cargar_lista_pacientes()

    def cargar_lista_pacientes(self):
        pacientes = self.model.get_todos_pacientes()
        self.view.actualizar_lista_pacientes(pacientes)

    def seleccionar_paciente(self, id_paciente, nombre_paciente):
        """Al clickear un paciente a la izquierda"""
        self.view.limpiar_form() # Limpiar form anterior
        self.paciente_seleccionado_id = id_paciente
        self.view.lbl_paciente_seleccionado.config(text=f"Expediente de: {nombre_paciente}")
        self._recargar_historial()

    def seleccionar_registro_historial(self, id_historial, diagnostico, tratamiento):
        """Al clickear un registro del historial a la derecha"""
        self.registro_seleccionado_id = id_historial
        self.view.llenar_form(diagnostico, tratamiento)

    def _recargar_historial(self):
        if self.paciente_seleccionado_id:
            historial = self.model.get_historial_medico(self.paciente_seleccionado_id)
            self.view.actualizar_historial(historial)

    def gestion_historial(self, accion):
        """Maneja Crear, Actualizar y Eliminar"""
        
        # 1. Validaciones Comunes
        if not self.paciente_seleccionado_id:
            messagebox.showwarning("!", "Seleccione un paciente primero.")
            return

        diag = self.view.txt_diag.get("1.0", "end-1c").strip()
        trat = self.view.txt_trat.get("1.0", "end-1c").strip()

        # 2. Lógica por Acción
        if accion == "crear":
            if not diag or not trat:
                messagebox.showerror("Error", "Llene diagnóstico y tratamiento.")
                return
            
            # Buscar cita vinculada (Regla de negocio DB)
            id_cita = self.model.get_ultima_cita_id(self.paciente_seleccionado_id)
            if not id_cita:
                messagebox.showerror("Error BD", "El paciente no tiene citas registradas. No se puede crear historial.")
                return

            if self.model.guardar_consulta(id_cita, diag, trat, self.doctor_id):
                messagebox.showinfo("Éxito", "Nuevo registro agregado.")
                self._post_accion()

        elif accion == "actualizar":
            if not self.registro_seleccionado_id:
                messagebox.showwarning("!", "Seleccione un registro del historial para editar.")
                return
            
            if self.model.actualizar_historial(self.registro_seleccionado_id, diag, trat):
                messagebox.showinfo("Éxito", "Registro actualizado.")
                self._post_accion()

        elif accion == "eliminar":
            if not self.registro_seleccionado_id:
                messagebox.showwarning("!", "Seleccione un registro del historial para eliminar.")
                return
            
            confirm = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro del historial?")
            if confirm:
                if self.model.eliminar_historial(self.registro_seleccionado_id):
                    messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")
                    self._post_accion()

    def _post_accion(self):
        """Limpieza después de una acción exitosa"""
        self.view.limpiar_form()
        self._recargar_historial()