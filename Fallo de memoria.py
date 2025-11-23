import tkinter as tk

class PantallaInicio(tk.Frame):
    def __init__(self, master, mostrar_vista_principal):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        self.frame_botones = tk.Frame(self, bg="white")
        self.frame_botones.pack(pady=40)

        self.btn_usuario = tk.Button(self.frame_botones, text="Usuario", width=10, height=5, font=("Arial", 12))
        self.btn_usuario.pack(side="left", padx=20)

        self.btn_admin = tk.Button(self.frame_botones, text="Administrador", width=10, height=5, font=("Arial", 12), command=mostrar_vista_principal)
        self.btn_admin.pack(side="left", padx=20)

        self.label_hola = tk.Label(self, text="HOLA!!", font=("Arial", 20, "bold"), bg="white")
        self.label_hola.pack(pady=30)

class VistaEstadisticas(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        self.label_titulo = tk.Label(self, text="ESTADÍSTICAS", font=("Arial", 18, "bold"), bg="white")
        self.label_titulo.pack(pady=(10, 0))

        self.label_dias = tk.Label(self, text="LUN MAR MIE JUE VIE", font=("Arial", 12), bg="white")
        self.label_dias.pack(pady=(5, 0))

        # Simulación de gráfica
        self.canvas = tk.Canvas(self, width=220, height=70, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=5)
        # Dibuja una línea y puntos simulando la gráfica
        puntos = [(10, 50), (50, 55), (90, 55), (130, 30), (170, 60)]
        self.canvas.create_line(*sum(puntos, ()), fill="black", width=2)
        for x, y in puntos:
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black")

        self.label_porcentajes = tk.Label(self, text="100% 80% 80% 100% 50%", font=("Arial", 10), bg="white")
        self.label_porcentajes.pack()

        self.label_semana = tk.Label(self, text="ESTA SEMANA", font=("Arial", 12, "bold"), bg="white")
        self.label_semana.pack(pady=(10, 0))

        self.label_mes = tk.Label(self, text="84% DE TAREAS COMPLETADAS\nESTE MES", font=("Arial", 12), bg="white")
        self.label_mes.pack(pady=(5, 0))

        self.boton_volver = tk.Button(self, text="Volver", command=volver_callback)
        self.boton_volver.pack(side="bottom", pady=10)

class VistaAnadirRecordatorio(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        self.label_titulo = tk.Label(self, text="AÑADIR RECORDATORIO", font=("Arial", 14, "bold"), bg="white")
        self.label_titulo.pack(pady=(10, 0))

        self.label_titulo2 = tk.Label(self, text="Título", font=("Arial", 10), bg="white")
        self.label_titulo2.pack()
        self.entry_titulo = tk.Entry(self, font=("Arial", 12))
        self.entry_titulo.pack(pady=2)

        self.label_hora = tk.Label(self, text="Hora", font=("Arial", 10), bg="white")
        self.label_hora.pack()
        self.entry_hora = tk.Entry(self, font=("Arial", 12), width=5)
        self.entry_hora.insert(0, "10:05")
        self.entry_hora.pack(pady=2)

        self.label_dias = tk.Label(self, text="Días de recordatorio", font=("Arial", 10), bg="white")
        self.label_dias.pack()
        self.frame_dias = tk.Frame(self, bg="white")
        self.frame_dias.pack()
        for dia in ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]:
            tk.Checkbutton(self.frame_dias, text=dia, bg="white").pack(side="left")

        self.check_mantener = tk.Checkbutton(self, text="Mantener", bg="white")
        self.check_mantener.pack(pady=2)

        self.check_alarma = tk.Checkbutton(self, text="Alarma", bg="white")
        self.check_alarma.pack(pady=2)

        self.label_sonido = tk.Label(self, text="Sonido:", font=("Arial", 10), bg="white")
        self.label_sonido.pack()
        self.sonido_var = tk.StringVar(value="JHON CENA SATURED")
        self.option_sonido = tk.OptionMenu(self, self.sonido_var, "JHON CENA SATURED", "Otro sonido")
        self.option_sonido.pack()

        self.boton_volver = tk.Button(self, text="Volver", command=volver_callback)
        self.boton_volver.pack(side="bottom", pady=10)

class VistaPrincipal(tk.Frame):
    def __init__(self, master, mostrar_estadisticas, mostrar_anadir_recordatorio):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)
        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        self.frame_botones = tk.Frame(self, bg="white")
        self.frame_botones.pack(expand=True)

        self.btn_registro_hoy = tk.Button(self.frame_botones, text="REGISTRO HOY", width=25, height=2, font=("Arial", 12, "bold"))
        self.btn_registro_hoy.pack(pady=10)

        self.btn_registro_anter = tk.Button(self.frame_botones, text="REGISTRO ANTERIOR", width=25, height=2, font=("Arial", 12, "bold"))
        self.btn_registro_anter.pack(pady=10)

        self.btn_anadir_recorda = tk.Button(self.frame_botones, text="AÑADIR RECORDATORIO", width=25, height=2, font=("Arial", 12, "bold"), command=mostrar_anadir_recordatorio)
        self.btn_anadir_recorda.pack(pady=10)

        self.btn_estadisticas = tk.Button(self.frame_botones, text="ESTADÍSTICAS", width=25, height=2, font=("Arial", 12, "bold"), command=mostrar_estadisticas)
        self.btn_estadisticas.pack(pady=10)

        self.bottom_bar = tk.Frame(self, bg="white", height=40)
        self.bottom_bar.pack(fill="x", side="bottom")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x450")
        self.resizable(False, False)
        self.config(bg="white")
        self.title("Administrador")

        self.pantalla_inicio = PantallaInicio(self, self.mostrar_vista_principal)
        self.vista_principal = None
        self.vista_estadisticas = None
        self.vista_anadir_recordatorio = None

    def mostrar_vista_principal(self):
        self.limpiar_frames()
        self.vista_principal = VistaPrincipal(self, self.mostrar_estadisticas, self.mostrar_anadir_recordatorio)

    def mostrar_estadisticas(self):
        self.limpiar_frames()
        self.vista_estadisticas = VistaEstadisticas(self, self.mostrar_vista_principal)

    def mostrar_anadir_recordatorio(self):
        self.limpiar_frames()
        self.vista_anadir_recordatorio = VistaAnadirRecordatorio(self, self.mostrar_vista_principal)

    def limpiar_frames(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

