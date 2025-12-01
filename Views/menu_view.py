import tkinter as tk
from tkinter import ttk

class MainMenuView(ttk.Frame):
    """
    Vista del menú principal que se carga después del login.
    """
    # Definición de Colores
    COLOR_SECONDARY = "#B2D9C4" 
    COLOR_ACCENT = "#44916F"    
    COLOR_TEXT_PRIMARY = "#247D7F" 
    COLOR_PRIMARY = "#C29470"   

    def __init__(self, master, controller, options, role):
        # 🚨 El parámetro 'role' es esencial para el constructor
        super().__init__(master, padding="30", style="Menu.TFrame") 
        
        self.master = master
        self.controller = controller # Referencia al MainController
        self.options = options
        self.role = role # Almacenamiento del rol
        
        self.master.title(f"Menú Principal - {role} | Consultorio Médico")
        self.master.geometry("800x600") 
        self.master.resizable(False, False)
        
        self._configure_styles()
        self.pack(expand=True, fill='both')
        self._create_widgets()

    def _configure_styles(self):
        """Configura los estilos TTK usando la paleta de colores."""
        style = ttk.Style()
        style.configure("Menu.TFrame", background=self.COLOR_SECONDARY)
        style.configure("MenuHeader.TLabel", 
                        background=self.COLOR_SECONDARY, 
                        foreground=self.COLOR_TEXT_PRIMARY, 
                        font=("Arial", 20, "bold"))

        #
        style.configure("Module.TButton", 
                        background=self.COLOR_ACCENT, 
                        foreground=self.COLOR_TEXT_PRIMARY,
                        font=("Arial", 14, "bold"),
                        padding=[20, 10], 
                        relief="flat")
        style.map("Module.TButton", 
                  background=[('active', self.COLOR_TEXT_PRIMARY)])

        style.configure("Logout.TButton", 
                        background=self.COLOR_PRIMARY, 
                        foreground=self.COLOR_TEXT_PRIMARY, 
                        font=("Arial", 10, "bold"))
        style.map("Logout.TButton", 
                  background=[('active', '#A07050')])


    def _create_widgets(self):
        """Crea el layout con la imagen central y los botones."""
        
        main_content_frame = ttk.Frame(self, style="Menu.TFrame")
        main_content_frame.pack(expand=True, fill=tk.BOTH)
        main_content_frame.columnconfigure(0, weight=1)
        main_content_frame.columnconfigure(1, weight=1)
        
        # --- Título y Rol ---
        ttk.Label(main_content_frame, text="Sistema de Gestión de Consultorio", style="MenuHeader.TLabel") \
           .grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=20, sticky="ew")
           
        ttk.Label(main_content_frame, text=f"Rol: {self.role}", style="MenuHeader.TLabel", font=("Arial", 12, "italic")) \
           .grid(row=1, column=0, columnspan=2, pady=(0, 20), padx=20, sticky="ew")

        # --- Imagen Central ---
        ttk.Label(main_content_frame, 
                  text="Consultorio Galeno", 
                  background="#D0E9DD", 
                  foreground=self.COLOR_TEXT_PRIMARY,
                  font=("Arial", 20),
                  anchor=tk.CENTER,
                  relief=tk.RIDGE,
                  padding=50)\
           .grid(row=2, column=0, columnspan=2, pady=10, padx=50, sticky="nsew")

        # --- Contenedor de Botones (RBAC) ---
        buttons_container = ttk.Frame(main_content_frame, style="Menu.TFrame")
        buttons_container.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        
        buttons_container.columnconfigure(0, weight=1)
        buttons_container.columnconfigure(1, weight=1)
        
        current_row = 0
        current_col = 0
        
        for title, command in self.options:
            ttk.Button(buttons_container, 
                       text=title, 
                       command=command, 
                       style="Module.TButton") \
               .grid(row=current_row, column=current_col, 
                     pady=10, padx=15, sticky="ew")
            
            current_col = 1 - current_col 
            if current_col == 0:
                current_row += 1 
            
        # --- Botón de Logout ---
        ttk.Button(self, 
                   text="Cerrar Sesión", 
                   command=self._logout_command, 
                   style="Logout.TButton") \
           .place(relx=0.98, rely=0.98, anchor=tk.SE)
           
    def _logout_command(self):
        """Maneja el cierre de sesión."""
        for widget in self.master.winfo_children():
            widget.destroy()
        
        self.controller.current_user = None
        self.controller.show_login()