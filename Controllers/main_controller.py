from Models.user_model import UserModel
from Views.login_view import LoginView

# Agrega las importaciones de otros controladores a medida que los crees
# from controllers.cita_controller import CitaController 
# from controllers.expediente_controller import ExpedienteController 


class MainController:
    """
    Controlador central de la aplicación.
    Maneja el inicio de sesión, la autenticación y el enrutamiento 
    a los módulos permitidos según el rol.
    """
    
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel() # Inicializa el Modelo de Usuarios
        self.current_user = None  # Almacenará los datos del usuario logueado
        
        # 1. Configuración de la Ventana Raíz (para que solo se vea el login)
        self.root.geometry("1x1") 
        self.root.withdraw() # Esconde la ventana raíz inmediatamente
        
        # 2. Iniciar la vista de Login
        self.show_login()
    
    
    def show_login(self):
        """Muestra la interfaz de inicio de sesión."""
        
        # Asegura que la ventana principal esté lista para recibir el LoginView (Frame)
        self.root.deiconify() 
        
        # Limpiar el contenido anterior (si ya se usó un menú)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear el LoginView (que ahora es un Frame y se empaqueta en el root)
        self.login_view = LoginView(self.root, self)
        
    
    def handle_login(self, Email, Password):
        """
        Maneja la solicitud de login desde la vista.
        """
        
        user_data = self.user_model.get_user_by_credentials(Email, Password)
        
        if user_data:
            self.current_user = user_data
            
            # Destruimos el Frame de LoginView, dejando el root limpio
            self.login_view.destroy() 
            
            print(f"✅ Login exitoso. Rol: {self.current_user['Nombre_Rol']}")
            
            # Proceder al menú principal/router
            self.show_main_menu(self.current_user['Nombre_Rol'])
        else:
            # Notificar a la vista del error
            self.login_view.show_error("Credenciales incorrectas o usuario no encontrado.")

    def show_main_menu(self, role):
        """
        Carga la vista del menú principal con opciones filtradas según el rol.
        """
        
        # Limpiar el contenido anterior (LoginView)
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 1. Definir las opciones y comandos (RBAC)
        options = []
        if role == 'Administrador':
            options = [
                ("Gestión de Pacientes", self.open_pacientes_module),
                ("Facturación y Pagos", self.open_facturacion_module),
                ("Reportes de Ocupación", self.open_reportes_module)
            ]
        elif role == 'Recepcionista':
            options = [
                ("Gestión de Pacientes", self.open_pacientes_module),
                ("Programación de Citas", self.open_citas_module),
                ("Facturación y Pagos", self.open_facturacion_module)
            ]
        elif role == 'Doctor':
            options = [
                ("Expediente Clínico", self.open_expediente_module)
            ]
            
        # 2. Cargar el menú principal con las opciones filtradas
       # self.main_menu_view = MainMenuView(self.root, self, options, role)


    # --- Métodos de Enrutamiento ---
    
    def open_pacientes_module(self):
        """Abre la ventana de Gestión de Pacientes."""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 🚨 Implementación del Controlador del Módulo
        #self.paciente_controller = PacienteController(self.root, self)
        print("✅ Módulo de Gestión de Pacientes cargado.")
        
    def open_citas_module(self):
        print("Abriendo Programación de Citas...")
        
    def open_facturacion_module(self):
        print("Abriendo Facturación y Pagos...")

    def open_expediente_module(self):
        print("Abriendo Expediente Clínico...")
        
    def open_reportes_module(self):
        # Validación de seguridad, aunque el botón ya está filtrado
        if self.current_user and self.current_user['Nombre_Rol'] == 'Administrador':
            print("Abriendo Reportes de Ocupación...")
        else:
            print("ACCESO DENEGADO a Reportes.")

    def __del__(self):
        """Cierra la conexión a la DB al terminar la aplicación."""
        if self.user_model:
            self.user_model.close_connection()