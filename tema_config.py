"""
Configuración de tema minimalista para el Sistema Médico
Paleta de colores profesional y suave
"""

# Paleta de colores minimalista
THEME = {
    # Colores principales
    "primary": "#2C3E50",      # Azul oscuro profesional
    "secondary": "#34495E",    # Gris azulado
    "accent": "#5D6D7E",       # Gris medio

    # Fondos
    "bg": "#ECF0F1",           # Gris muy claro (fondo principal)
    "white": "#FFFFFF",        # Blanco puro
    "card": "#FFFFFF",         # Fondo de tarjetas

    # Texto
    "text": "#2C3E50",         # Texto oscuro principal
    "text_light": "#7F8C8D",   # Texto secundario

    # Bordes y separadores
    "border": "#BDC3C7",       # Borde sutil
    "divider": "#D5DBDB",      # Líneas divisorias

    # Estados
    "success": "#27AE60",      # Verde suave (éxito)
    "warning": "#F39C12",      # Naranja suave (advertencia)
    "danger": "#E74C3C",       # Rojo suave (error)
    "info": "#3498DB",         # Azul suave (información)

    # Hover y activos
    "hover": "#34495E",        # Color al pasar el mouse
    "active": "#2C3E50",       # Color cuando está activo
}

# Fuentes
FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 14, "bold"),
    "heading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "button": ("Segoe UI", 11),
}

# Espaciado
SPACING = {
    "xs": 5,
    "sm": 10,
    "md": 15,
    "lg": 20,
    "xl": 30,
}
