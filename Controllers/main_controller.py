
from Models.user_model import UserModel
from Views.login_view import LoginView
from Controllers.cita_controller import CitaController

## esta clase manejara la autenticacion y las vistas a las que tiene acceso cada usuario
class MainController:
    """
    Controlador central de la aplicación.
    Maneja el inicio de sesión, la autenticación y el enrutamiento 
    a los módulos permitidos según el rol.
    """
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()
        self.current_user = None  # Almacenará los datos del usuario logueado (ID, Nombre, Rol)
        
        # 1. Configurar la ventana principal de Tkinter
        self.root.title("Sistema de Gestión de Consultorio Médico")
        
        # 2. Iniciar la vista de Login
        self.show_login()

    def show_login(self):
        """Muestra la interfaz de inicio de sesión."""
        # Cerrar cualquier ventana o menú previo (si aplica)
        # Aquí iniciaremos la vista de Login, pasándole este controlador
        # para que la vista pueda llamar al método handle_login
        self.login_view = LoginView(self.root, self)
        
    def handle_login(self, email, password):
        """
        Maneja la solicitud de login desde la vista.
        """
        
        # 1. Llamar al Modelo para autenticar
        user_data = self.user_model.get_user_by_credentials(email, password)
        
        if user_data:
            self.current_user = user_data
            self.login_view.destroy() # Cerrar la ventana de Login
            print(f"✅ Login exitoso. Rol: {self.current_user['Nombre_Rol']}")
            
            # 2. Proceder al menú principal/router
            self.open_citas_module()
        
        else:
            # 3. Notificar a la vista del error
            self.login_view.show_error("Credenciales incorrectas o usuario no encontrado.")

    def show_main_menu(self, role):
        """
        Carga la vista del menú principal o el módulo directo según el rol.
        Aquí se implementa el Control de Acceso Basado en Roles (RBAC).
        """
        # Nota: Por ahora, solo mostraremos un mensaje, 
        # pero aquí cargarías la clase views.main_menu_view.py
        print(f"--- Cargando Menú Principal para {role} ---")
        


    
    def open_pacientes_module(self):
        print("Abriendo Gestión de Pacientes...")
        # Lógica: Cargar views.paciente_view y su controlador.
        
    def open_citas_module(self):
        print("Abriendo Programación de Citas...")
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cargar el controlador
        self.cita_controller = CitaController(self.root, self)
        print("✅ Módulo de Programación de Citas cargado.")
        
        
    def open_reportes_module(self):
        if self.current_user and self.current_user['Nombre_Rol'] == 'Administrador':
            print("Abriendo Reportes de Ocupación...")
        else:
            # Esto es una validación de seguridad extra en el controlador
            print("ACCESO DENEGADO a Reportes.")

    def __del__(self):
        """Cierra la conexión a la DB al terminar la aplicación."""
        if self.user_model:
            self.user_model.close_connection()