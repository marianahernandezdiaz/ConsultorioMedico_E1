import tkinter as tk
from tkinter import ttk

class MainMenuView(ttk.Frame):
    """
    Vista del menú principal que se carga después del login.
    """
    # Paleta minimalista profesional
    COLOR_PRIMARY = "#2C3E50"      # Azul oscuro profesional
    COLOR_SECONDARY = "#34495E"    # Gris azulado
    COLOR_ACCENT = "#5D6D7E"       # Gris medio
    COLOR_BG = "#ECF0F1"           # Gris muy claro
    COLOR_WHITE = "#FFFFFF"        # Blanco
    COLOR_TEXT = "#2C3E50"         # Texto oscuro
    COLOR_BORDER = "#BDC3C7"       # Borde sutil

    def __init__(self, master, controller, options, role):
        super().__init__(master, padding="0", style="Menu.TFrame")

        self.master = master
        self.controller = controller
        self.options = options
        self.role = role

        self.master.title(f"Sistema Médico - {role}")
        self.master.geometry("900x600")
        self.master.resizable(False, False)

        self._configure_styles()
        self.pack(expand=True, fill='both')
        self._create_widgets()

    def _configure_styles(self):
        """Configura los estilos TTK usando la paleta de colores."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Menu.TFrame", background=self.COLOR_BG)

        style.configure("Header.TFrame", background=self.COLOR_PRIMARY)

        style.configure("MenuHeader.TLabel",
                        background=self.COLOR_PRIMARY,
                        foreground=self.COLOR_WHITE,
                        font=("Segoe UI", 24, "bold"))

        style.configure("MenuSubtitle.TLabel",
                        background=self.COLOR_PRIMARY,
                        foreground=self.COLOR_BG,
                        font=("Segoe UI", 10))

        style.configure("Module.TButton",
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_TEXT,
                        font=("Segoe UI", 12),
                        padding=[30, 15],
                        borderwidth=1,
                        relief="flat")
        style.map("Module.TButton",
                  background=[('active', self.COLOR_SECONDARY)],
                  foreground=[('active', self.COLOR_WHITE)])

        style.configure("Logout.TButton",
                        background=self.COLOR_ACCENT,
                        foreground=self.COLOR_WHITE,
                        font=("Segoe UI", 9),
                        padding=[15, 8])
        style.map("Logout.TButton",
                  background=[('active', self.COLOR_SECONDARY)])


    def _create_widgets(self):
        """Crea el layout con la imagen central y los botones."""

        # --- Header ---
        header_frame = ttk.Frame(self, style="Header.TFrame")
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="Sistema de Gestión Médica", style="MenuHeader.TLabel") \
           .pack(pady=(20, 5))

        ttk.Label(header_frame, text=f"Usuario: {self.role}", style="MenuSubtitle.TLabel") \
           .pack(pady=(0, 20))

        # --- Contenedor principal ---
        main_content_frame = ttk.Frame(self, style="Menu.TFrame")
        main_content_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)
        main_content_frame.columnconfigure(0, weight=1)
        main_content_frame.columnconfigure(1, weight=1)

        # --- Título de sección ---
        ttk.Label(main_content_frame,
                  text="Módulos Disponibles",
                  background=self.COLOR_BG,
                  foreground=self.COLOR_TEXT,
                  font=("Segoe UI", 14, "bold")) \
           .grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # --- Contenedor de Botones (RBAC) ---
        buttons_container = ttk.Frame(main_content_frame, style="Menu.TFrame")
        buttons_container.grid(row=1, column=0, columnspan=2, sticky="nsew")

        buttons_container.columnconfigure(0, weight=1)
        buttons_container.columnconfigure(1, weight=1)

        current_row = 0
        current_col = 0

        for title, command in self.options:
            ttk.Button(buttons_container,
                       text=title,
                       command=command,
                       style="Module.TButton",
                       cursor="hand2") \
               .grid(row=current_row, column=current_col,
                     pady=8, padx=10, sticky="ew")

            current_col = 1 - current_col
            if current_col == 0:
                current_row += 1

        # --- Botón de Logout ---
        ttk.Button(self,
                   text="Cerrar Sesión",
                   command=self._logout_command,
                   style="Logout.TButton",
                   cursor="hand2") \
           .place(relx=0.95, rely=0.95, anchor=tk.SE)
           
    def _logout_command(self):
        """Maneja el cierre de sesión."""
        for widget in self.master.winfo_children():
            widget.destroy()
        
        self.controller.current_user = None
        self.controller.show_login()