import tkinter as tk
from tkinter import ttk, messagebox

PALETTE = {
    "primary": "#247D7F",
    "secondary": "#44916F",
    "accent": "#B2D9C4",
    "bg": "#80B9C8",
    "warn": "#C29470",
}

class LoginView(tk.Toplevel):
    """
    Interfaz gráfica de inicio de sesión.
    Hereda de tk.Toplevel para ser una ventana secundaria que se abre sobre la principal.
    """
    def __init__(self, master, controller):
        # Llama al constructor de Toplevel
        super().__init__(master)
        
        self.master = master
        self.controller = controller
        
        # 1. Configuración básica de la ventana de Login
        self.title("Inicio de Sesión")
        self.geometry("350x250")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"]) 
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=PALETTE["bg"]) 
        style.configure("TLabel", background=PALETTE["bg"], foreground="#0F3D3E")
        style.configure("Primary.TButton", padding=8, foreground="white", background=PALETTE["primary"]) 
        style.map("Primary.TButton", background=[("active", PALETTE["secondary"])])
        style.configure("Form.TEntry", fieldbackground="#FFFFFF")
        
        # Centrar la ventana en la pantalla (opcional)
        self.center_window()
        
        # Bloquea la ventana principal mientras el login está abierto
        self.transient(master) 
        self.grab_set() 
        
        # 2. Configurar el diseño (Grid)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        
        self._create_widgets()
        
    def center_window(self):
        """Calcula la posición para centrar la ventana en la pantalla."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (350/2))
        y_cordinate = int((screen_height/2) - (250/2))
        self.geometry(f"350x250+{x_cordinate}+{y_cordinate}")

    def _create_widgets(self):
        """Crea y coloca todos los elementos de la interfaz."""
        
        # --- Variables de entrada ---
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # --- 1. Título ---
        ttk.Label(self, text="Acceso al Sistema Médico", font=("Arial", 14, "bold")) \
           .grid(row=0, column=0, columnspan=2, pady=15, padx=10, sticky="nsew")

        # --- 2. Campo Email ---
        ttk.Label(self, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=30, style="Form.TEntry")
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.email_entry.focus() # Enfocar automáticamente

        # --- 3. Campo Contraseña ---
        ttk.Label(self, text="Contraseña:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*", width=30, style="Form.TEntry")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Permite iniciar sesión presionando Enter
        self.password_entry.bind('<Return>', lambda event: self._login_command())

        # --- 4. Botón de Login ---
        ttk.Button(self, text="Ingresar", style="Primary.TButton", command=self._login_command, cursor="hand2") \
           .grid(row=3, column=0, columnspan=2, pady=20)
        
    def _login_command(self):
        """
        Función llamada al presionar el botón Ingresar.
        Obtiene los datos y llama al método del controlador.
        """
        email = self.email_var.get()
        password = self.password_var.get()
        
        # Validar campos vacíos primero
        if not email or not password:
            self.show_error("Debe ingresar email y contraseña.")
            return

        # Llama al método del controlador, pasando las credenciales
        self.controller.handle_login(email, password)

    def show_error(self, message):
        """Muestra un mensaje de error usando messagebox de Tkinter."""
        messagebox.showerror("Error de Login", message, parent=self)
        
    def destroy(self):
        """Sobreescribe destroy para liberar el bloqueo y cerrar la ventana."""
        self.grab_release()
        super().destroy()
