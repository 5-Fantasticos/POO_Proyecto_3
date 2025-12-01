import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import tkinter.font as tkfont
from PIL import Image, ImageTk
import calendar

# Paleta Medisafe (igual que Interfaz.py)
BG = "#f4f8fb"
PRIMARY = "#2b87f0"
ACCENT = "#14c1a3"
CARD = "#ffffff"
TEXT = "#0f1722"
MUTED = "#6b7280"
SHADOW = "#e6eefc"

# Solo importa GestorEventos y Evento si están disponibles (para modo GUI)
try:
    from Modelo import GestorEventos, Evento
except ImportError:
    GestorEventos = None
    Evento = None

class Calendario:
    def __init__(self):
        self.eventos = {}
        self.root = None
        self.celdas = {}
        self.fecha_actual = datetime.today().replace(day=1)

    def mostrar_calendario_gui(self):
        self.root = tk.Tk()
        self._configurar_ventana()
        self._mostrar_calendario_gui()
        self.root.mainloop()

    def seleccionar_fecha(self, callback):
        self._callback_fecha = callback
        self.root = tk.Toplevel()
        self._configurar_ventana()
        self._mostrar_calendario_gui(seleccion=True)

    def _configurar_ventana(self):
        self.root.title("Seleccionar fecha")
        self.root.geometry("650x750")
        self.root.configure(bg=BG)
        # Fuente moderna
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=12)
        self.root.option_add("*Font", default_font)

    def _generar_semanas_mes(self):
        año = self.fecha_actual.year
        mes = self.fecha_actual.month
        primer_dia_semana, dias_mes = calendar.monthrange(año, mes)
        semanas = []
        semana_actual = []
        for _ in range(primer_dia_semana):
            semana_actual.append("")
        for dia in range(1, dias_mes + 1):
            semana_actual.append(str(dia))
            if len(semana_actual) == 7:
                semanas.append(semana_actual)
                semana_actual = []
        if semana_actual:
            while len(semana_actual) < 7:
                semana_actual.append("")
            semanas.append(semana_actual)
        return semanas

    def _mostrar_calendario_gui(self, seleccion=False):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.celdas = {}

        frame_cal = tk.Frame(self.root, bg=BG)
        frame_cal.pack(expand=True, fill="both", padx=40, pady=30)

        # --- Navegación de mes ---
        nav_frame = tk.Frame(frame_cal, bg=BG)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=(0, 10))
        btn_prev = tk.Button(nav_frame, text="◀", font=("Segoe UI", 14, "bold"), bg=BG, fg=PRIMARY, bd=0, command=self._mes_anterior, cursor="hand2")
        btn_prev.pack(side="left", padx=10)
        meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_actual = meses_es[self.fecha_actual.month - 1]
        label_mes = tk.Label(nav_frame, text=f"{mes_actual} {self.fecha_actual.year}", font=("Segoe UI", 22, "bold"), bg=BG, fg=PRIMARY)
        label_mes.pack(side="left", padx=20)
        btn_next = tk.Button(nav_frame, text="▶", font=("Segoe UI", 14, "bold"), bg=BG, fg=PRIMARY, bd=0, command=self._mes_siguiente, cursor="hand2")
        btn_next.pack(side="left", padx=10)

        # Días de la semana
        nombres_es = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
        for i, nombre in enumerate(nombres_es):
            tk.Label(frame_cal, text=nombre, width=10, height=2, borderwidth=1, relief="solid",
                     bg=BG, fg=PRIMARY, font=("Segoe UI", 12, "bold")).grid(row=1, column=i, padx=2, pady=2)

        semanas = self._generar_semanas_mes()
        for i, semana in enumerate(semanas):
            for j, dia in enumerate(semana):
                texto = dia if dia else ""
                lbl = tk.Label(
                    frame_cal,
                    text=texto,
                    borderwidth=1,
                    relief="solid",
                    width=10,
                    height=3,
                    bg=CARD if texto else BG,
                    fg=TEXT if texto else BG,
                    font=("Segoe UI", 13, "bold") if texto else ("Segoe UI", 13)
                )
                lbl.grid(row=i+2, column=j, padx=2, pady=2, sticky="nsew")
                if texto:
                    fecha_str = f"{self.fecha_actual.year}-{self.fecha_actual.month:02d}-{int(texto):02d}"
                    if seleccion:
                        lbl.bind("<Double-Button-1>", lambda e, f=fecha_str: self._seleccionar_fecha_callback(f))
                    else:
                        lbl.bind("<Double-Button-1>", lambda e, f=fecha_str: self.popup_crear_evento(f))
                self.celdas[f"{i}-{j}"] = lbl

        # Ajustar columnas y filas para expandirse
        for col in range(7):
            frame_cal.grid_columnconfigure(col, weight=1)
        for row in range(len(semanas) + 2):
            frame_cal.grid_rowconfigure(row, weight=1)

    def _mes_anterior(self):
        mes = self.fecha_actual.month - 1
        anio = self.fecha_actual.year
        if mes < 1:
            mes = 12
            anio -= 1
        self.fecha_actual = self.fecha_actual.replace(year=anio, month=mes, day=1)
        self._mostrar_calendario_gui(seleccion=True)

    def _mes_siguiente(self):
        mes = self.fecha_actual.month + 1
        anio = self.fecha_actual.year
        if mes > 12:
            mes = 1
            anio += 1
        self.fecha_actual = self.fecha_actual.replace(year=anio, month=mes, day=1)
        self._mostrar_calendario_gui(seleccion=True)

    def _seleccionar_fecha_callback(self, fecha):
        if hasattr(self, "_callback_fecha") and self._callback_fecha:
            self._callback_fecha(fecha)
        self.root.destroy()

    def popup_crear_evento(self, fecha):
        descripcion = simpledialog.askstring("Registrar evento", f"Descripción para {fecha}:")
        if descripcion:
            self.crear_evento(fecha, descripcion)
            messagebox.showinfo("Evento creado", f"Evento registrado para {fecha}.")
            self._mostrar_calendario_gui()

    def crear_evento(self, fecha, descripcion):
        if fecha not in self.eventos:
            self.eventos[fecha] = []
        self.eventos[fecha].append(descripcion)