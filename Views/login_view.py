import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, padding="30 20 30 20") 
        
        self.master = master
        self.controller = controller
        
        # Colores \
        self.COLOR_PRIMARY = "#C29470"  # Marrón claro
        self.COLOR_SECONDARY = "#B2D9C4" # Verde menta claro
        self.COLOR_ACCENT = "#44916F"   # Verde oscuro (botones/acentos)
        self.COLOR_TEXT_PRIMARY = "#247D7F" # Azul verdoso oscuro (texto)
        self.COLOR_BACKGROUND_LIGHT = "#F8F8F8" # Blanco
        self.COLOR_BLUE_LIGHT = "#80B9C8" # Azul claro

        # Configurar estilos de ttk
        self._configure_styles()
        
        self.pack(expand=True, fill='both')
        
        self.master.title("Clinica Médica - Login")
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        self.master.config(bg=self.COLOR_SECONDARY) 
        
        self._create_widgets()
        
    def _configure_styles(self):
        """Configura los estilos de los widgets ttk."""
        style = ttk.Style()
        
        # Fondo general del frame de login
        style.configure("TFrame", background=self.COLOR_SECONDARY)
        
        # Título
        style.configure("Title.TLabel", 
                        background=self.COLOR_SECONDARY, 
                        foreground=self.COLOR_TEXT_PRIMARY, 
                        font=("Arial", 18, "bold"),
                        anchor="center") 
        
        # Labels de Email/Contraseña
        style.configure("TLabel", 
                        background=self.COLOR_SECONDARY, 
                        foreground=self.COLOR_TEXT_PRIMARY,
                        font=("Arial", 11))
                        
        # Entradas de texto
        style.configure("TEntry", 
                        fieldbackground=self.COLOR_BACKGROUND_LIGHT, 
                        foreground="#333333",
                        font=("Arial", 11),
                        bordercolor=self.COLOR_PRIMARY,
                        borderwidth=1)
        
        # Botones
        style.configure("TButton", 
                        background=self.COLOR_ACCENT, 
                        foreground=self.COLOR_TEXT_PRIMARY, 
                        font=("Arial", 12, "bold"),
                        padding=10)
        style.map("TButton", 
                  background=[('active', self.COLOR_ACCENT)]) # Efecto hover
        
    def _create_widgets(self):
        """Crea y coloca todos los elementos de la interfaz."""
        
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Configurar el grid dentro del Frame para centrar
        self.columnconfigure(0, weight=1) # Columna de labels
        self.columnconfigure(1, weight=3) # Columna de entries
        
        # 1. Título
    
        ttk.Label(self, text="Acceso al Sistema Médico", style="Title.TLabel") \
           .grid(row=0, column=0, columnspan=2, pady=(15, 25), padx=10, sticky="nsew")

        # 2. Campo Email
        ttk.Label(self, text="Email:").grid(row=1, column=0, padx=(10, 5), pady=5, sticky="e") # Alineado a la derecha
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
        self.email_entry.focus()

        # 3. Campo Contraseña
        ttk.Label(self, text="Contraseña:").grid(row=2, column=0, padx=(10, 5), pady=5, sticky="e") # Alineado a la derecha
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="ew")
        self.password_entry.bind('<Return>', lambda event: self._login_command())

        # 4. Botón de Login
        ttk.Button(self, text="Ingresar", command=self._login_command, cursor="hand2") \
           .grid(row=3, column=0, columnspan=2, pady=30) 
        
    def _login_command(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            self.show_error("Debe ingresar email y contraseña.")
            return

        self.controller.handle_login(email, password)

    def show_error(self, message):
        messagebox.showerror("Error de Login", message, parent=self.master)