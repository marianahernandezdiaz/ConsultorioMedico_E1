import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(ttk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, padding="40 30 40 30")

        self.master = master
        self.controller = controller

        # Paleta minimalista profesional
        self.COLOR_PRIMARY = "#2C3E50"      # Azul oscuro profesional
        self.COLOR_SECONDARY = "#34495E"    # Gris azulado
        self.COLOR_ACCENT = "#5D6D7E"       # Gris medio
        self.COLOR_TEXT = "#2C3E50"         # Texto oscuro
        self.COLOR_BG = "#ECF0F1"           # Gris muy claro (fondo)
        self.COLOR_WHITE = "#FFFFFF"        # Blanco puro
        self.COLOR_SUCCESS = "#27AE60"      # Verde suave

        # Configurar estilos de ttk
        self._configure_styles()

        self.pack(expand=True, fill='both')

        self.master.title("Sistema Médico - Inicio de Sesión")
        self.master.geometry("450x380")
        self.master.resizable(False, False)
        self.master.config(bg=self.COLOR_BG)

        self._create_widgets()
        
    def _configure_styles(self):
        """Configura los estilos de los widgets ttk."""
        style = ttk.Style()
        style.theme_use('clam')

        # Fondo general del frame de login
        style.configure("TFrame", background=self.COLOR_BG)

        # Título
        style.configure("Title.TLabel",
                        background=self.COLOR_BG,
                        foreground=self.COLOR_PRIMARY,
                        font=("Segoe UI", 20, "bold"),
                        anchor="center")

        # Subtítulo
        style.configure("Subtitle.TLabel",
                        background=self.COLOR_BG,
                        foreground=self.COLOR_ACCENT,
                        font=("Segoe UI", 9),
                        anchor="center")

        # Labels de Email/Contraseña
        style.configure("TLabel",
                        background=self.COLOR_BG,
                        foreground=self.COLOR_TEXT,
                        font=("Segoe UI", 10))

        # Entradas de texto
        style.configure("TEntry",
                        fieldbackground=self.COLOR_WHITE,
                        foreground=self.COLOR_TEXT,
                        font=("Segoe UI", 10),
                        borderwidth=1,
                        relief="solid")

        # Botones
        style.configure("Login.TButton",
                        background=self.COLOR_PRIMARY,
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        borderwidth=0,
                        padding=12)
        style.map("Login.TButton",
                  background=[('active', self.COLOR_SECONDARY)])
        
    def _create_widgets(self):
        """Crea y coloca todos los elementos de la interfaz."""

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Configurar el grid dentro del Frame para centrar
        self.columnconfigure(0, weight=1)

        # Contenedor central con borde sutil
        container = ttk.Frame(self, style="TFrame")
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        container.columnconfigure(0, weight=1)

        # 1. Título
        ttk.Label(container, text="Sistema Médico", style="Title.TLabel") \
           .grid(row=0, column=0, pady=(0, 5), sticky="ew")

        ttk.Label(container, text="Inicio de Sesión", style="Subtitle.TLabel") \
           .grid(row=1, column=0, pady=(0, 30), sticky="ew")

        # 2. Campo Email
        ttk.Label(container, text="Correo Electrónico").grid(row=2, column=0, padx=5, pady=(10, 5), sticky="w")
        self.email_entry = ttk.Entry(container, textvariable=self.email_var, width=40)
        self.email_entry.grid(row=3, column=0, padx=5, pady=(0, 15), sticky="ew", ipady=8)
        self.email_entry.focus()

        # 3. Campo Contraseña
        ttk.Label(container, text="Contraseña").grid(row=4, column=0, padx=5, pady=(0, 5), sticky="w")
        self.password_entry = ttk.Entry(container, textvariable=self.password_var, show="●", width=40)
        self.password_entry.grid(row=5, column=0, padx=5, pady=(0, 25), sticky="ew", ipady=8)
        self.password_entry.bind('<Return>', lambda event: self._login_command())

        # 4. Botón de Login
        ttk.Button(container, text="INGRESAR", command=self._login_command,
                  style="Login.TButton", cursor="hand2") \
           .grid(row=6, column=0, padx=5, pady=(0, 10), sticky="ew") 
        
    def _login_command(self):
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            self.show_error("Debe ingresar email y contraseña.")
            return

        self.controller.handle_login(email, password)

    def show_error(self, message):
        messagebox.showerror("Error de Login", message, parent=self.master)