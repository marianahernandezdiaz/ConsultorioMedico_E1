import tkinter as tk 
from tkinter import ttk, messagebox

# Paleta de colores
PALETA = {
    "header": "#247D7F",       # Barra superior / títulos
    "fondo": "#B2D9C4",        # Fondo de la ventana
    "frame": "#80B9C8",        # Fondo del formulario
    "btn_principal": "#247D7F",
    "btn_secundario": "#44916F",
    "accent": "#C29470"
}


def abrir_ventana_insertar_paciente(master, controller):

    win = tk.Toplevel(master)
    win.title("Insertar Paciente")
    win.geometry("650x450")
    win.config(bg=PALETA["fondo"])
    win.grab_set()  # para que tenga el foco hasta cerrar

    # --------- Estilos ttk para botones ----------
    estilo = ttk.Style(win)
    estilo.theme_use("clam")

    estilo.configure(
        "Primary.TButton",
        background=PALETA["btn_principal"],
        foreground="white",
        padding=6
    )
    estilo.map(
        "Primary.TButton",
        background=[("active", PALETA["accent"])]
    )

    estilo.configure(
        "Secondary.TButton",
        background=PALETA["btn_secundario"],
        foreground="white",
        padding=6
    )
    estilo.map(
        "Secondary.TButton",
        background=[("active", PALETA["header"])]
    )

    # --------- Helper para crear filas de etiqueta + entry ----------
    def agregar_entrada_con_etiqueta(parent, texto_etiqueta, fila, ancho=30):
        tk.Label(
            parent,
            text=texto_etiqueta,
            bg=PALETA["frame"],
            anchor="w",
            font=("Arial", 10, "bold")  # Etiquetas en negrita
        ).grid(row=fila, column=0, sticky="w", pady=5, padx=5)

        entrada = tk.Entry(parent, width=ancho)
        entrada.grid(row=fila, column=1, sticky="w", pady=5, padx=5)
        return entrada

    # --------- Header ----------
    header = tk.Frame(win, bg=PALETA["header"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Registro de nuevo paciente",
        bg=PALETA["header"],
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # --------- Formulario ----------
    frame_form = tk.Frame(win, bg=PALETA["frame"], padx=15, pady=15, bd=0)
    frame_form.pack(fill="both", expand=True, padx=20, pady=(15, 5))

    frame_form.columnconfigure(0, weight=0)
    frame_form.columnconfigure(1, weight=1)

    # Campos que SÍ existen en la tabla Pacientes
    entrada_nombres = agregar_entrada_con_etiqueta(frame_form, "Nombres:", 0)
    entrada_apellidos = agregar_entrada_con_etiqueta(frame_form, "Apellidos:", 1)

    # Fecha de nacimiento (texto simple con formato YYYY-MM-DD)
    tk.Label(
        frame_form,
        text="Fecha de nacimiento (YYYY-MM-DD):",
        bg=PALETA["frame"],
        anchor="w",
        font=("Arial", 10, "bold")  # Etiqueta en negrita
    ).grid(row=2, column=0, sticky="w", pady=5, padx=5)

    entrada_fecha_nac = tk.Entry(frame_form, width=20)
    entrada_fecha_nac.grid(row=2, column=1, sticky="w", pady=5, padx=5)

    # Ajustamos el tamaño de los campos de entrada para que todos sean del mismo tamaño
    entrada_telefono = agregar_entrada_con_etiqueta(frame_form, "Teléfono:", 3)
    entrada_direccion = agregar_entrada_con_etiqueta(frame_form, "Dirección:", 4, ancho=40)
    entrada_seguro = agregar_entrada_con_etiqueta(frame_form, "Seguro médico:", 5)

    # --------- Guardar ----------
    def guardar_paciente():
        nombres = entrada_nombres.get().strip()
        apellidos = entrada_apellidos.get().strip()
        fecha_nac = entrada_fecha_nac.get().strip()

        if not nombres or not apellidos or not fecha_nac:
            messagebox.showwarning(
                "Campos obligatorios",
                "Nombres, Apellidos y Fecha de nacimiento son obligatorios."
            )
            return

        datos = {
            "nombres": nombres,
            "apellidos": apellidos,
            "fecha_nac": fecha_nac,  # formato 'YYYY-MM-DD'
            "telefono": entrada_telefono.get().strip(),
            "direccion": entrada_direccion.get().strip(),
            "seguro_med": entrada_seguro.get().strip(),
        }

        try:
            controller.insertar_paciente(datos)
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar:\n{e}")

    # --------- Botones ---------
    frame_botones = tk.Frame(win, bg=PALETA["fondo"])
    frame_botones.pack(side="bottom", pady=10)

    ttk.Button(
        frame_botones,
        text="Guardar",
        style="Primary.TButton",
        command=guardar_paciente
    ).grid(row=0, column=0, padx=10, pady=5)

    ttk.Button(
        frame_botones,
        text="Cancelar",
        style="Secondary.TButton",
        command=win.destroy
    ).grid(row=0, column=1, padx=10, pady=5)
