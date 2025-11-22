import tkinter as tk

class VistaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x450")
        self.resizable(False, False)
        self.config(bg="white")

        # Simulación de barra superior
        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        # Botones principales
        self.frame_botones = tk.Frame(self, bg="white")
        self.frame_botones.pack(expand=True)

        self.btn_registro_hoy = tk.Button(self.frame_botones, text="REGISTRO HOY", width=25, height=2, font=("Arial", 12, "bold"))
        self.btn_registro_hoy.pack(pady=10)

        self.btn_registro_anter = tk.Button(self.frame_botones, text="REGISTRO ANTERIOR", width=25, height=2, font=("Arial", 12, "bold"))
        self.btn_registro_anter.pack(pady=10)

        self.btn_anadir_recorda = tk.Button(self.frame_botones, text="AÑADIR RECORDATORIO", width=25, height=2, font=("Arial", 12, "bold"))
        self.btn_anadir_recorda.pack(pady=10)

        self.btn_estadisticas = tk.Button(self.frame_botones, text="ESTADÍSTICAS", width=25, height=2, font=("Arial", 12, "bold"))
        self.btn_estadisticas.pack(pady=10)

        # Barra inferior simulada
        self.bottom_bar = tk.Frame(self, bg="white", height=40)
        self.bottom_bar.pack(fill="x", side="bottom")
        # Iconos simulados
        self.icon1 = tk.Label(self.bottom_bar, text="◀", font=("Arial", 18), bg="white")
        self.icon1.pack(side="left", expand=True)
        self.icon2 = tk.Label(self.bottom_bar, text="⬤", font=("Arial", 18), bg="white")
        self.icon2.pack(side="left", expand=True)
        self.icon3 = tk.Label(self.bottom_bar, text="▢", font=("Arial", 18), bg="white")
        self.icon3.pack(side="left", expand=True)

if __name__ == "__main__":
    app = VistaPrincipal()
    app.mainloop()

