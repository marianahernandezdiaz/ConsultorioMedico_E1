import tkinter as tk 
from tkinter import ttk, messagebox
import sys, os

# Para poder importar tema_config igual que en DoctorView
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tema_config import THEME


def abrir_ventana_insertar_paciente(master, controller):

    win = tk.Toplevel(master)
    win.title("Insertar Paciente")
    win.geometry("700x480")
    win.config(bg=THEME["bg"])
    win.grab_set()  # para que tenga el foco hasta cerrar

    # --------- Estilos ttk para botones y entries ----------
    estilo = ttk.Style(win)
    estilo.theme_use("clam")

    # Botón principal (Guardar)
    estilo.configure(
        "Primary.TButton",
        background=THEME["success"],
        foreground="white",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )
    estilo.map(
        "Primary.TButton",
        background=[("active", THEME["accent"])]
    )

    # Botón secundario (Cancelar)
    estilo.configure(
        "Secondary.TButton",
        background=THEME["secondary"],
        foreground="white",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )
    estilo.map(
        "Secondary.TButton",
        background=[("active", THEME["primary"])]
    )

    # Estilo para Entry (para que combine con el tema)
    estilo.configure(
        "TEntry",
        fieldbackground=THEME["white"],
        foreground=THEME["text"],
        borderwidth=1
    )

    # --------- Helper para crear filas de etiqueta + entry ----------
    def agregar_entrada_con_etiqueta(parent, texto_etiqueta, fila, ancho=30):
        tk.Label(
            parent,
            text=texto_etiqueta,
            bg=THEME["white"],
            fg=THEME["text"],
            anchor="w",
            font=("Segoe UI", 10, "bold")
        ).grid(row=fila, column=0, sticky="w", pady=5, padx=5)

        entrada = ttk.Entry(parent, width=ancho)
        entrada.grid(row=fila, column=1, sticky="ew", pady=5, padx=5)
        return entrada

    # --------- Header ----------
    header = tk.Frame(win, bg=THEME["primary"])
    header.pack(fill="x")

    tk.Label(
        header,
        text="Registro de nuevo paciente",
        bg=THEME["primary"],
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=12)

    # --------- Contenedor principal ----------
    contenedor = tk.Frame(win, bg=THEME["bg"])
    contenedor.pack(fill="both", expand=True, padx=20, pady=(15, 10))

    # --------- Formulario ----------
    frame_form = tk.Frame(contenedor, bg=THEME["white"], padx=20, pady=20, bd=1, relief=tk.SOLID)
    frame_form.pack(fill="both", expand=True)

    frame_form.columnconfigure(0, weight=0)
    frame_form.columnconfigure(1, weight=1)

    # Campos que SÍ existen en la tabla Pacientes
    entrada_nombres = agregar_entrada_con_etiqueta(frame_form, "Nombres:", 0)
    entrada_apellidos = agregar_entrada_con_etiqueta(frame_form, "Apellidos:", 1)

    # Fecha de nacimiento (texto simple con formato YYYY-MM-DD)
    tk.Label(
        frame_form,
        text="Fecha de nacimiento (YYYY-MM-DD):",
        bg=THEME["white"],
        fg=THEME["text"],
        anchor="w",
        font=("Segoe UI", 10, "bold")
    ).grid(row=2, column=0, sticky="w", pady=5, padx=5)

    entrada_fecha_nac = ttk.Entry(frame_form, width=20)
    entrada_fecha_nac.grid(row=2, column=1, sticky="w", pady=5, padx=5)

    entrada_telefono = agregar_entrada_con_etiqueta(frame_form, "Teléfono:", 3)

    # Dirección ocupa más ancho
    tk.Label(
        frame_form,
        text="Dirección:",
        bg=THEME["white"],
        fg=THEME["text"],
        anchor="w",
        font=("Segoe UI", 10, "bold")
    ).grid(row=4, column=0, sticky="nw", pady=5, padx=5)

    entrada_direccion = ttk.Entry(frame_form)
    entrada_direccion.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

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
    frame_botones = tk.Frame(contenedor, bg=THEME["bg"])
    frame_botones.pack(fill="x", pady=(10, 5))

    frame_botones.columnconfigure(0, weight=1)
    frame_botones.columnconfigure(1, weight=0)
    frame_botones.columnconfigure(2, weight=0)

    ttk.Button(
        frame_botones,
        text="Guardar",
        style="Primary.TButton",
        command=guardar_paciente
    ).grid(row=0, column=1, padx=10, pady=5, sticky="e")

    ttk.Button(
        frame_botones,
        text="Cancelar",
        style="Secondary.TButton",
        command=win.destroy
    ).grid(row=0, column=2, padx=10, pady=5, sticky="e")
