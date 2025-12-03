# Controllers/PacientesController.py

from datetime import datetime
import re

from Models.GestionPacientesModel import GestionPacientesModel


class PacienteController:
    def __init__(self):
        self.model = GestionPacientesModel()

    # ==============================
    # MÉTODOS PÚBLICOS (usados por las vistas)
    # ==============================

    def insertar_paciente(self, datos_formulario):
        """
        Recibe los datos de la vista InsertarPaciente y los manda al modelo.
        datos_formulario debe tener:
            - nombres
            - apellidos
            - fecha_nac
            - telefono
            - direccion
            - seguro_med
        """

        # --- Validaciones ---
        nombres = self._validar_cadena(datos_formulario.get("nombres"), "Nombres", requerido=True, max_len=100)
        apellidos = self._validar_cadena(datos_formulario.get("apellidos"),"Apellidos",requerido=True, max_len=100)
        fecha_nac = self._validar_fecha(datos_formulario.get("fecha_nac"),"Fecha de nacimiento")
        telefono = self._validar_telefono(datos_formulario.get("telefono"),"Teléfono",requerido=False)
        direccion = self._validar_cadena(datos_formulario.get("direccion"),"Dirección",requerido=False,max_len=200)
        seguro_med = self._validar_cadena(datos_formulario.get("seguro_med"),"Seguro médico",requerido=False,max_len=100)

        datos_limpios = {
            "nombres": nombres,
            "apellidos": apellidos,
            "fecha_nac": fecha_nac,   # 
            "telefono": telefono,
            "direccion": direccion,
            "seguro_med": seguro_med,
        }

        nuevo_id = self.model.insertar_paciente(datos_limpios)
        print(f">>> Paciente insertado con ID: {nuevo_id}")
        return nuevo_id

    def obtener_paciente_por_id(self, id_paciente: int):
        """
        Pide al modelo los datos de un paciente por su ID.
        """
        id_valido = self._validar_entero(id_paciente, "ID de paciente", minimo=1)
        return self.model.obtener_paciente_por_id(id_valido)

    def actualizar_paciente(self, id_paciente: int, datos: dict) -> bool:
        """
        Actualiza un paciente usando el modelo.
        """

        id_valido = self._validar_entero(id_paciente, "ID de paciente", minimo=1)

        nombres = self._validar_cadena(datos.get("nombres"),"Nombres",requerido=True,max_len=100)
        apellidos = self._validar_cadena(datos.get("apellidos"),"Apellidos",requerido=True,max_len=100)
        fecha_nac = self._validar_fecha(datos.get("fecha_nac"),"Fecha de nacimiento")
        telefono = self._validar_telefono(datos.get("telefono"),"Teléfono",requerido=False)
        direccion = self._validar_cadena(datos.get("direccion"),"Dirección",requerido=False,max_len=200)
        seguro_med = self._validar_cadena(datos.get("seguro_med"),"Seguro médico",requerido=False,max_len=100)

        datos_limpios = {
            "nombres": nombres,
            "apellidos": apellidos,
            "fecha_nac": fecha_nac,
            "telefono": telefono,
            "direccion": direccion,
            "seguro_med": seguro_med,
        }

        return self.model.actualizar_paciente(id_valido, datos_limpios)

    def eliminar_paciente(self, id_paciente: int) -> bool:
        """
        Elimina un paciente usando el modelo.
        """
        id_valido = self._validar_entero(id_paciente, "ID de paciente", minimo=1)
        return self.model.eliminar_paciente(id_valido)
    

    def listar_pacientes(self):
        """
        Pide al modelo la lista completa de pacientes.
        """
        return self.model.listar_pacientes()

    # ==============================
    # MÉTODOS PRIVADOS DE VALIDACIÓN
    # ==============================

    def _validar_entero(self, valor, nombre_campo: str, minimo=None, maximo=None) -> int:
        """
        Valida que valor sea un entero (o convertible) y opcionalmente dentro de un rango.
        Lanza ValueError con un mensaje entendible si no es válido.
        """
        if isinstance(valor, str):
            valor = valor.strip()

        if valor is None or valor == "":
            raise ValueError(f"{nombre_campo} es obligatorio.")

        try:
            num = int(valor)
        except (TypeError, ValueError):
            raise ValueError(f"{nombre_campo} debe ser un número entero.")

        if minimo is not None and num < minimo:
            raise ValueError(f"{nombre_campo} debe ser mayor o igual a {minimo}.")

        if maximo is not None and num > maximo:
            raise ValueError(f"{nombre_campo} debe ser menor o igual a {maximo}.")

        return num

    def _validar_cadena(self, valor, nombre_campo: str, requerido=True, max_len=None) -> str | None:
        """
        Valida que sea una cadena (si es requerida) y que no exceda un máximo de caracteres.
        Devuelve la cadena limpia (stripped) o None si no es requerida y viene vacía.
        """
        if valor is None:
            if requerido:
                raise ValueError(f"{nombre_campo} es obligatorio.")
            return None

        texto = str(valor).strip()

        if requerido and texto == "":
            raise ValueError(f"{nombre_campo} es obligatorio.")

        if not requerido and texto == "":
            return None

        if max_len is not None and len(texto) > max_len:
            raise ValueError(
                f"{nombre_campo} no debe exceder los {max_len} caracteres."
            )

        return texto

    def _validar_fecha(self, valor, nombre_campo: str) -> str:
        """
        Valida que la fecha venga en formato 'YYYY-MM-DD'.
        Devuelve la misma cadena si es válida.
        """
        if not valor:
            raise ValueError(f"{nombre_campo} es obligatoria.")

        valor = str(valor).strip()

        try:
            # Verificamos el formato correcto
            datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"{nombre_campo} debe tener el formato YYYY-MM-DD (ejemplo: 1990-05-21)."
            )

        return valor

    def _validar_telefono(self, valor, nombre_campo: str, requerido=False) -> str | None:
        """
        Valida un teléfono sencillo: opcionalmente requerido, solo dígitos y longitud razonable.
        Devuelve el string limpio o None si está vacío y no es requerido.
        """
        if valor is None:
            if requerido:
                raise ValueError(f"{nombre_campo} es obligatorio.")
            return None

        tel = str(valor).strip()

        if tel == "":
            if requerido:
                raise ValueError(f"{nombre_campo} es obligatorio.")
            return None

        # Permitimos solo dígitos, +, espacios y guiones si quieres
        # Aquí uso solo dígitos para mantenerlo simple.
        if not re.fullmatch(r"\d{7,15}", tel):
            raise ValueError(
                f"{nombre_campo} debe contener solo dígitos y tener entre 7 y 15 caracteres."
            )

        return tel
