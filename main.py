

import tkinter as tk
import sys
import os

# 1. Ajuste de Ruta (para robustez del entorno)
# Esto asegura que Python pueda encontrar las carpetas 'controllers', 'models', 'views'
# sin importar cómo se inicie el script en VS Code o en la terminal.
# Aunque se recomienda ejecutar desde la raíz, este código da soporte extra.
sys.path.append(os.path.dirname(__file__))

# 2. Importación del Controlador Principal
# La importación absoluta funciona porque la línea de arriba agregó la raíz al PATH.
from Controllers.main_controller import MainController

if __name__ == "__main__":
    
    # 3. Inicializar la Ventana Raíz (Tkinter)
    # Esta es la ventana principal que contendrá todas las demás vistas.
    root = tk.Tk()
    
    # 4. Inicializar el Controlador Principal
    # Le pasamos la ventana raíz (root). El MainController se encarga de:
    #   a) Mostrar la vista de Login (LoginView).
    #   b) Manejar la autenticación.
    #   c) Abrir el menú o módulo correcto según el rol.
    app = MainController(root) 
    
    # 5. Iniciar el Bucle Principal (Tkinter Event Loop)
    # Esto hace que la ventana de Tkinter se mantenga abierta y responda a eventos.
    root.mainloop()

    # 6. Lógica de limpieza
    # Aseguramos que el controlador cierre la conexión a la base de datos cuando la app termina.
    if app and hasattr(app, '__del__'):
        app.__del__()