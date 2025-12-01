import tkinter as tk
from datetime import datetime
from modelo import *
from tkinter import messagebox
    
# Pantalla de inicio con opciones de usuario y administrador
class PantallaInicio(tk.Frame):
    def __init__(self, master, mostrar_vista_principal):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        # Barra superior
        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        # Botones de usuario y administrador
        self.frame_botones = tk.Frame(self, bg="white")
        self.frame_botones.pack(pady=40)

        self.btn_usuario = tk.Button(
            self.frame_botones,
            text="Usuario",
            width=10,
            height=5,
            font=("Arial", 12),
            command=master.mostrar_vista_usuario  # ← aquí añadimos el comando
        )
        self.btn_usuario.pack(side="left", padx=20)

        self.btn_admin = tk.Button(self.frame_botones, text="Administrador", width=10, height=5, font=("Arial", 12), command=mostrar_vista_principal)
        self.btn_admin.pack(side="left", padx=20)

        # Saludo
        self.label_hola = tk.Label(self, text="HOLA!!", font=("Arial", 20, "bold"), bg="white")
        self.label_hola.pack(pady=30)

# Vista de estadísticas (por lo visto solo tiene datos ya listo, eso al final se cambiara para que usurio ingrese sus propios datos)
class VistaEstadisticas(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        # Barra superior
        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")
        
        # Titulo de la vista
        self.label_titulo = tk.Label(self, text="ESTADÍSTICAS", font=("Arial", 18, "bold"), bg="white")
        self.label_titulo.pack(pady=(10, 0))

        # Dias de la semana
        self.label_dias = tk.Label(self, text="LUN MAR MIE JUE VIE", font=("Arial", 12), bg="white")
        self.label_dias.pack(pady=(5, 0))

        # Simulación de gráfica
        self.canvas = tk.Canvas(self, width=220, height=70, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=5) # canvas para dibujar la grafica

        # Dibuja una línea y puntos simulando la gráfica
        puntos = [(10, 50), (50, 55), (90, 55), (130, 30), (170, 60)]
        self.canvas.create_line(*sum(puntos, ()), fill="black", width=2)
        for x, y in puntos:
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black")

        # Texto de porcentajes debajo de la grafica y otros textos informativos
        self.label_porcentajes = tk.Label(self, text="100% 80% 80% 100% 50%", font=("Arial", 10), bg="white")
        self.label_porcentajes.pack()

        self.label_semana = tk.Label(self, text="ESTA SEMANA", font=("Arial", 12, "bold"), bg="white")
        self.label_semana.pack(pady=(10, 0))

        self.label_mes = tk.Label(self, text="84% DE TAREAS COMPLETADAS\nESTE MES", font=("Arial", 12), bg="white")
        self.label_mes.pack(pady=(5, 0))

        # Boton para volver a la vista principal
        self.boton_volver = tk.Button(self, text="Volver", command=volver_callback)
        self.boton_volver.pack(side="bottom", pady=10)

# Vista para añadir un nuevo recordatorio
class VistaAnadirRecordatorio(tk.Frame): 
    def __init__(self, master, volver_callback): 
        super().__init__(master, bg="white") 
        self.pack(fill="both", expand=True) 

        # Barra superior
        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        # Titulo de la vista
        self.label_titulo = tk.Label(self, text="AÑADIR RECORDATORIO", font=("Arial", 14, "bold"), bg="white")
        self.label_titulo.pack(pady=(10, 0))

        # Campos para ingresar los detalles del recordatorio
        self.label_titulo2 = tk.Label(self, text="Título", font=("Arial", 10), bg="white")
        self.label_titulo2.pack()
        self.entry_titulo = tk.Entry(self, font=("Arial", 12))
        self.entry_titulo.pack(pady=2)

        # Campo para la hora
        self.label_hora = tk.Label(self, text="Hora", font=("Arial", 10), bg="white")
        self.label_hora.pack()
        self.entry_hora = tk.Entry(self, font=("Arial", 12), width=5)
        self.entry_hora.insert(0, "10:05")
        self.entry_hora.pack(pady=2)

        # Campo para seleccionar los días de recordatorio
        self.label_dias = tk.Label(self, text="Días de recordatorio", font=("Arial", 10), bg="white")
        self.label_dias.pack()
        self.frame_dias = tk.Frame(self, bg="white")
        self.frame_dias.pack()

        self.check_vars = {}  # Diccionario para guardar las variables de cada día
        for dia in ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.frame_dias, text=dia, variable=var, bg="white")
            cb.pack(side="left")
            self.check_vars[dia] = var

        # Opciones adicionales
        self.var_mantener = tk.BooleanVar()
        self.check_mantener = tk.Checkbutton(self, text="Mantener", variable=self.var_mantener, bg="white")
        self.check_mantener.pack(pady=2)

        self.var_alarma = tk.BooleanVar()
        self.check_alarma = tk.Checkbutton(self, text="Alarma", variable=self.var_alarma, bg="white")
        self.check_alarma.pack(pady=2)

        # Opción para seleccionar el sonido
        self.label_sonido = tk.Label(self, text="Sonido:", font=("Arial", 10), bg="white")
        self.label_sonido.pack()
        self.sonido_var = tk.StringVar(value="JHON CENA SATURED")
        self.option_sonido = tk.OptionMenu(self, self.sonido_var, "JHON CENA SATURED", "Otro sonido")
        self.option_sonido.pack()

        # Botón Añadir
        self.boton_añadir = tk.Button(self, text="Añadir", command=self.guardar_recordatorio)
        self.boton_añadir.pack(pady=10)

        # Botón Volver
        self.boton_volver = tk.Button(self, text="Volver", command=volver_callback)
        self.boton_volver.pack(side="bottom", pady=10)

    def guardar_recordatorio(self):
        titulo = self.entry_titulo.get()
        hora = self.entry_hora.get()
        dias = [dia for dia, var in self.check_vars.items() if var.get()]
        mantener = self.var_mantener.get()
        alarma = self.var_alarma.get()
        sonido = self.sonido_var.get()
        creador = "Administrador"  # o "Usuario" si implementas roles

        if not titulo or not hora:
            messagebox.showerror("Error", "Título y hora son obligatorios")
            return

        evento = Evento(titulo, hora, dias, creador, estado="pendiente", nombre_alarma=sonido)
        evento.guardar()
        messagebox.showinfo("Éxito", "Recordatorio añadido correctamente")


# Vista principal con opciones para el administrador
class VistaPrincipal(tk.Frame):
    def __init__(self, master, mostrar_estadisticas, mostrar_anadir_recordatorio): 
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True) # Expande el frame para llenar la ventana

        # Barra superior
        self.top_bar = tk.Frame(self, bg="white", height=30)
        self.top_bar.pack(fill="x", side="top")

        # Barra de botones principales
        self.frame_botones = tk.Frame(self, bg="white")
        self.frame_botones.pack(expand=True)

        # Botones para las diferentes opciones
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

        self.btn_volver_inicio = tk.Button(self.bottom_bar, text="Volver al inicio", command=master.mostrar_inicio)
        self.btn_volver_inicio.pack(pady=5)

# Aplicación principal que maneja las diferentes vistas
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("350x450") # Tamaño de la ventana
        self.resizable(False, False) 
        self.config(bg="white")
        self.title("Administrador")

        # Pantalla de inicio
        self.pantalla_inicio = PantallaInicio(self, self.mostrar_vista_principal)
        self.vista_principal = None
        self.vista_estadisticas = None
        self.vista_anadir_recordatorio = None
     
    # Función para mostrar la vista principal
    def mostrar_vista_principal(self):
        self.limpiar_frames()
        self.vista_principal = VistaPrincipal(self, self.mostrar_estadisticas, self.mostrar_anadir_recordatorio)

    # Función para mostrar la vista de estadísticas
    def mostrar_estadisticas(self):
        self.limpiar_frames()
        self.vista_estadisticas = VistaEstadisticas(self, self.mostrar_vista_principal)

    # Función para mostrar la vista de añadir recordatorio
    def mostrar_anadir_recordatorio(self):
        self.limpiar_frames()
        self.vista_anadir_recordatorio = VistaAnadirRecordatorio(self, self.mostrar_vista_principal)

    # Función para limpiar los frames actuales
    def limpiar_frames(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def mostrar_vista_usuario(self):
        self.limpiar_frames()
        self.vista_usuario = VistaUsuario(self, self.mostrar_inicio)
    
    def mostrar_inicio(self):
        self.limpiar_frames()
        self.pantalla_inicio = PantallaInicio(self, self.mostrar_vista_principal)

# Vista para el usuario que muestra sus recordatorios
class VistaUsuario(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master, bg="white")
        self.pack(fill="both", expand=True)

        self.label_titulo = tk.Label(self, text="RECORDATORIOS DEL USUARIO", font=("Arial", 14, "bold"), bg="white")
        self.label_titulo.pack(pady=10)

        eventos = Evento.leer_eventos_json()

        if not eventos:
            tk.Label(self, text="No hay recordatorios guardados", bg="white").pack(pady=10)
        else:
            self.eventos_json = eventos  # Guardamos los datos para saber qué se selecciona
            self.lista = tk.Listbox(self, width=40, height=10, selectmode=tk.MULTIPLE)
            self.lista.pack(pady=10)
            for e in eventos:
                texto = f"{e['hora']} - {e['titulo']} ({', '.join(e['dias'])})"
                if e["estado"] == "completado":
                    texto += " ✅"
                self.lista.insert(tk.END, texto)

            self.btn_marcar = tk.Button(self, text="Marcar como realizado", command=self.marcar_realizado)
            self.btn_marcar.pack(pady=5)

        self.btn_volver_inicio = tk.Button(self, text="Volver al inicio", command=volver_callback)
        self.btn_volver_inicio.pack(pady=10)

    # Función para marcar tareas como realizadas
    def marcar_realizado(self):
        seleccionados = self.lista.curselection()
        if not seleccionados:
            messagebox.showinfo("Aviso", "Selecciona al menos una tarea")
            return

        eventos = Evento.leer_eventos_json()
        for i in seleccionados:
            eventos[i]["estado"] = "completado"
            Evento.registrar_historial(eventos[i]["titulo"], "Usuario", "marco como realizado")

        with open("eventos.json", "w", encoding="utf-8") as f:
            json.dump(eventos, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Éxito", "Tareas marcadas como realizadas")
        self.master.mostrar_vista_usuario()  # Recarga la vista



# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()

