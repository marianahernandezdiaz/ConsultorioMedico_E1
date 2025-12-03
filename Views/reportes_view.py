import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from Models.db_manager import DBManager

PALETTE = {
    "primary": "#247D7F",
    "accent": "#44916F",
    "bg": "#B2D9C4",
    "muted": "#80B9C8",
    "contrast": "#C29470",
}

class ReportesView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Reportes de Ocupación")
        self.geometry("900x620")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.db = DBManager()

        self.configure(bg=PALETTE["bg"])
        self.columnconfigure(0, weight=1)
        self._build_header()
        self._build_filters()
        self._build_kpis()
        self._build_tables()
        self._refresh()

    def _build_header(self):
        header = tk.Frame(self, bg=PALETTE["primary"])
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        title = tk.Label(header, text="Reportes de Ocupación", fg="white", bg=PALETTE["primary"], font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, padx=16, pady=12, sticky="w")

    def _build_filters(self):
        bar = tk.Frame(self, bg=PALETTE["bg"])
        bar.grid(row=1, column=0, sticky="ew", padx=16, pady=8)
        ttk.Label(bar, text="Rango:").grid(row=0, column=0, padx=(0,8))
        self.range_cb = ttk.Combobox(bar, values=["Hoy", "Últimos 7 días", "Este mes", "Todo"], state="readonly")
        self.range_cb.current(1)
        self.range_cb.grid(row=0, column=1)
        self.update_btn = ttk.Button(bar, text="Actualizar", command=self._refresh)
        self.update_btn.grid(row=0, column=2, padx=8)

    def _build_kpis(self):
        wrap = tk.Frame(self, bg=PALETTE["bg"]) 
        wrap.grid(row=2, column=0, sticky="ew", padx=16)
        for i in range(3):
            wrap.columnconfigure(i, weight=1)
        self.kpi_total = self._kpi_card(wrap, 0, "Citas en rango", PALETTE["accent"]) 
        self.kpi_completadas = self._kpi_card(wrap, 1, "Completadas", PALETTE["primary"]) 
        self.kpi_productividad = self._kpi_card(wrap, 2, "% Productividad", PALETTE["muted"]) 

    def _kpi_card(self, parent, col, title, color):
        frame = tk.Frame(parent, bg=color)
        frame.grid(row=0, column=col, sticky="ew", padx=8, pady=8)
        tk.Label(frame, text=title, bg=color, fg="white", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        value = tk.Label(frame, text="-", bg=color, fg="white", font=("Arial", 20, "bold"))
        value.pack(anchor="w", padx=10, pady=(0,10))
        return value

    def _build_tables(self):
        tables = tk.Frame(self, bg=PALETTE["bg"]) 
        tables.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8,16))
        tables.columnconfigure(0, weight=1)
        tables.columnconfigure(1, weight=1)

        left = ttk.Frame(tables)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,8))
        ttk.Label(left, text="Frecuencia de citas por día").grid(row=0, column=0, sticky="w", pady=(0,6))
        self.day_tv = ttk.Treeview(left, columns=("fecha","total"), show="headings", height=12)
        self.day_tv.heading("fecha", text="Fecha")
        self.day_tv.heading("total", text="Total")
        self.day_tv.column("fecha", width=140)
        self.day_tv.column("total", width=80, anchor="center")
        self.day_tv.grid(row=1, column=0, sticky="nsew")

        right = ttk.Frame(tables)
        right.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        ttk.Label(right, text="Productividad por doctor").grid(row=0, column=0, sticky="w", pady=(0,6))
        self.doc_tv = ttk.Treeview(right, columns=("doctor","tot","comp","prod"), show="headings", height=12)
        self.doc_tv.heading("doctor", text="Doctor")
        self.doc_tv.heading("tot", text="Citas")
        self.doc_tv.heading("comp", text="Completadas")
        self.doc_tv.heading("prod", text="%")
        self.doc_tv.column("doctor", width=180)
        self.doc_tv.column("tot", width=80, anchor="center")
        self.doc_tv.column("comp", width=110, anchor="center")
        self.doc_tv.column("prod", width=60, anchor="center")
        self.doc_tv.grid(row=1, column=0, sticky="nsew")

        ttk.Button(self, text="Cerrar", command=self._close).grid(row=4, column=0, pady=(0,16))

    def _range_dates(self):
        today = date.today()
        key = self.range_cb.get()
        if key == "Hoy":
            return today, today
        if key == "Últimos 7 días":
            return today - timedelta(days=6), today
        if key == "Este mes":
            start = today.replace(day=1)
            end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            return start, end
        return date(1970,1,1), date(2100,1,1)

    def _refresh(self):
        start, end = self._range_dates()
        day_rows = self.db.execute_query(
            "SELECT Fecha, COUNT(*) AS total FROM Citas WHERE Fecha BETWEEN %s AND %s GROUP BY Fecha ORDER BY Fecha",
            (start, end)
        )
        tot_rows = self.db.execute_query(
            "SELECT COUNT(*) AS tot FROM Citas WHERE Fecha BETWEEN %s AND %s",
            (start, end)
        )
        comp_rows = self.db.execute_query(
            "SELECT COUNT(*) AS comp FROM Historial_Medico H JOIN Citas C ON H.ID_Cita=C.ID_Cita WHERE C.Fecha BETWEEN %s AND %s",
            (start, end)
        )
        doc_tot = self.db.execute_query(
            "SELECT U.ID_Usuario AS id, U.Nombre_usuario AS doctor, COUNT(*) AS tot FROM Citas C JOIN Usuarios U ON C.ID_Doctor=U.ID_Usuario WHERE C.Fecha BETWEEN %s AND %s GROUP BY U.ID_Usuario, U.Nombre_usuario ORDER BY tot DESC",
            (start, end)
        )
        doc_comp = self.db.execute_query(
            "SELECT U.ID_Usuario AS id, COUNT(*) AS comp FROM Historial_Medico H JOIN Citas C ON H.ID_Cita=C.ID_Cita JOIN Usuarios U ON H.ID_Doctor=U.ID_Usuario WHERE C.Fecha BETWEEN %s AND %s GROUP BY U.ID_Usuario",
            (start, end)
        )
        comp_map = {r["id"]: r["comp"] for r in doc_comp}

        total = tot_rows[0]["tot"] if tot_rows else 0
        completadas = comp_rows[0]["comp"] if comp_rows else 0
        productividad = round((completadas/total*100) if total else 0, 1)

        self.kpi_total.config(text=str(total))
        self.kpi_completadas.config(text=str(completadas))
        self.kpi_productividad.config(text=f"{productividad}%")

        for i in self.day_tv.get_children():
            self.day_tv.delete(i)
        for r in day_rows:
            self.day_tv.insert("", "end", values=(str(r["Fecha"]), r["total"]))

        for i in self.doc_tv.get_children():
            self.doc_tv.delete(i)
        for r in doc_tot:
            comp = comp_map.get(r["id"], 0)
            prod = round((comp/r["tot"]*100) if r["tot"] else 0, 1)
            self.doc_tv.insert("", "end", values=(r["doctor"], r["tot"], comp, f"{prod}%"))

    def _close(self):
        if self.db:
            self.db.close()
        self.destroy()
