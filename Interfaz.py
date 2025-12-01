import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recordatorios")
        self.geometry("600x700")
        self.configure(bg="#24102b")
        self.frames = {}
        for F in (InicioScreen, UsuarioScreen, PrincipalScreen, RealizadasScreen, RecordatorioScreen, ListaRecordatoriosScreen):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        self.cambiar_pantalla("InicioScreen")

    def cambiar_pantalla(self, nombre):
        for f in self.frames.values():
            f.place_forget()
        self.frames[nombre].place(relwidth=1, relheight=1)

    # Métodos de ejemplo para enlazar con botones
    def leer_pendientes(self):
        pass

    def mostrar_lista(self, modo):
        self.cambiar_pantalla("ListaRecordatoriosScreen")

    def crear_recordatorio(self):
        pass

    def cambiar_filtro_realizadas(self, filtro):
        pass

    def cambiar_filtro_dia_realizadas(self, dia):
        pass

    def cambiar_filtro_semana_realizadas(self, semana):
        pass

    def cambiar_filtro_mes_realizadas(self, mes):
        pass

# Widgets personalizados
def dark_label(parent, text, size=14, bold=False):
    font = ("Arial", size, "bold" if bold else "normal")
    return tk.Label(parent, text=text, fg="white", bg="#24102b", font=font)

def info_label(parent, text, size=12):
    return tk.Label(parent, text=text, fg="white", bg="#24102b", anchor="w", font=("Arial", size))

def colored_button(parent, text, command=None, size=14):
    return tk.Button(parent, text=text, fg="white", bg="#660080", font=("Arial", size), command=command, relief="flat", activebackground="#4d0066")

def day_toggle(parent, text, var):
    return tk.Checkbutton(parent, text=text, fg="white", bg="#24102b", selectcolor="#660080", variable=var, font=("Arial", 10, "bold"))

# Pantallas
class InicioScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#24102b")
        tk.Label(self, bg="#24102b").pack(pady=20)
        dark_label(self, "HOLA!!", size=24, bold=True).pack(pady=10)
        btn_frame = tk.Frame(self, bg="#24102b")
        btn_frame.pack(pady=30)
        colored_button(btn_frame, "Usuario", lambda: master.cambiar_pantalla("UsuarioScreen"), size=18).grid(row=0, column=0, padx=20, ipadx=10, ipady=10)
        colored_button(btn_frame, "Administrador", lambda: master.cambiar_pantalla("PrincipalScreen"), size=18).grid(row=0, column=1, padx=20, ipadx=10, ipady=10)

class UsuarioScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#24102b")
        dark_label(self, "Recordatorios Pendientes", size=20, bold=True).pack(pady=10)
        tk.Frame(self, height=35, bg="#24102b").pack()
        cont = tk.Frame(self, bg="#24102b")
        cont.pack(expand=True, fill="both")
        self.usuario_cont = tk.Frame(cont, bg="#24102b")
        self.usuario_cont.pack(expand=True, fill="both")
        colored_button(self, "Leer pendientes", master.leer_pendientes, size=14).pack(pady=8, ipadx=10, ipady=5)
        colored_button(self, "Volver", lambda: master.cambiar_pantalla("InicioScreen"), size=14).pack(pady=8, ipadx=10, ipady=5)

class PrincipalScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#24102b")
        tk.Frame(self, height=80, bg="#24102b").pack()
        btn_frame = tk.Frame(self, bg="#24102b")
        btn_frame.pack(pady=20)
        colored_button(btn_frame, "Tareas realizadas", lambda: master.cambiar_pantalla("RealizadasScreen"), size=20).pack(fill="x", pady=7, ipadx=10, ipady=10)
        colored_button(btn_frame, "Crear Recordatorio", lambda: master.cambiar_pantalla("RecordatorioScreen"), size=20).pack(fill="x", pady=7, ipadx=10, ipady=10)
        colored_button(btn_frame, "Eliminar Recordatorio", lambda: master.mostrar_lista("eliminar"), size=20).pack(fill="x", pady=7, ipadx=10, ipady=10)
        colored_button(btn_frame, "Modificar Recordatorio", lambda: master.mostrar_lista("modificar"), size=20).pack(fill="x", pady=7, ipadx=10, ipady=10)
        colored_button(btn_frame, "Inicio", lambda: master.cambiar_pantalla("InicioScreen"), size=16).pack(fill="x", pady=7, ipadx=10, ipady=7)

class ListaRecordatoriosScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#24102b")
        dark_label(self, "Selecciona un recordatorio", size=18, bold=True).pack(pady=10)
        self.contenedor_lista = tk.Frame(self, bg="#24102b")
        self.contenedor_lista.pack(expand=True, fill="both")
        colored_button(self, "Volver", lambda: master.cambiar_pantalla("PrincipalScreen"), size=14).pack(pady=10, ipadx=10, ipady=5)

class RealizadasScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#24102b")
        dark_label(self, "Tareas realizadas", size=20, bold=True).pack(pady=10)
        filtro_frame = tk.Frame(self, bg="#24102b")
        filtro_frame.pack(pady=5)
        self.filtro_realizadas = tk.StringVar(value="prioritarias")
        tk.Radiobutton(filtro_frame, text="Prioritarias", variable=self.filtro_realizadas, value="prioritarias", fg="white", bg="#24102b", selectcolor="#660080", command=lambda: master.cambiar_filtro_realizadas("prioritarias")).pack(side="left", padx=5)
        tk.Radiobutton(filtro_frame, text="Secundarias", variable=self.filtro_realizadas, value="secundarias", fg="white", bg="#24102b", selectcolor="#660080", command=lambda: master.cambiar_filtro_realizadas("secundarias")).pack(side="left", padx=5)
        # Filtros por día
        dias_frame = tk.Frame(self, bg="#24102b")
        dias_frame.pack(pady=5)
        self.filtro_dia = tk.StringVar(value="todos")
        for dia in ["Todos", "LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]:
            tk.Radiobutton(dias_frame, text=dia, variable=self.filtro_dia, value=dia, fg="white", bg="#24102b", selectcolor="#660080", command=lambda d=dia: master.cambiar_filtro_dia_realizadas(d)).pack(side="left", padx=2)
        # Filtro semana
        semana_frame = tk.Frame(self, bg="#24102b")
        semana_frame.pack(pady=5)
        tk.Label(semana_frame, text="Semana:", fg="white", bg="#24102b", width=8).pack(side="left")
        self.semana_var = tk.StringVar(value="todas")
        semana_spn = ttk.Combobox(semana_frame, textvariable=self.semana_var, values=["todas", "Semana 1", "Semana 2", "Semana 3", "Semana 4"], width=10)
        semana_spn.pack(side="left")
        semana_spn.bind("<<ComboboxSelected>>", lambda e: master.cambiar_filtro_semana_realizadas(self.semana_var.get()))
        # Filtro mes
        mes_frame = tk.Frame(self, bg="#24102b")
        mes_frame.pack(pady=5)
        tk.Label(mes_frame, text="Mes:", fg="white", bg="#24102b", width=8).pack(side="left")
        self.mes_var = tk.StringVar(value="todos")
        meses = ["todos","enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
        mes_spn = ttk.Combobox(mes_frame, textvariable=self.mes_var, values=meses, width=12)
        mes_spn.pack(side="left")
        mes_spn.bind("<<ComboboxSelected>>", lambda e: master.cambiar_filtro_mes_realizadas(self.mes_var.get()))
        # Lista de tareas realizadas
        self.realizadas_cont = tk.Frame(self, bg="#24102b")
        self.realizadas_cont.pack(expand=True, fill="both", pady=10)
        colored_button(self, "Volver", lambda: master.cambiar_pantalla("PrincipalScreen"), size=14).pack(pady=10, ipadx=10, ipady=5)

class RecordatorioScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#24102b")
        cont = tk.Frame(self, bg="#24102b")
        cont.pack(expand=True, fill="both", padx=16, pady=10)
        dark_label(cont, "AÑADIR RECORDATORIO", size=18, bold=True).pack(pady=5)
        info_label(cont, "Título").pack(anchor="w")
        self.titulo_input = tk.Entry(cont, font=("Arial", 12))
        self.titulo_input.pack(fill="x", pady=2)
        info_label(cont, "Hora (HH:MM)").pack(anchor="w")
        self.hora_input = tk.Entry(cont, font=("Arial", 12))
        self.hora_input.insert(0, "10:05")
        self.hora_input.pack(fill="x", pady=2)
        info_label(cont, "Repetir").pack(anchor="w")
        self.repetir_var = tk.StringVar(value="No repetir")
        ttk.Combobox(cont, textvariable=self.repetir_var, values=["No repetir","Diariamente","Semanalmente","Mensualmente"]).pack(fill="x", pady=2)
        imp_frame = tk.Frame(cont, bg="#24102b")
        imp_frame.pack(fill="x", pady=2)
        info_label(imp_frame, "Importante").pack(side="left")
        self.importante_chk = tk.BooleanVar()
        tk.Checkbutton(imp_frame, variable=self.importante_chk, bg="#24102b", selectcolor="#660080").pack(side="left")
        info_label(cont, "Días de recordatorio").pack(anchor="w")
        dias_frame = tk.Frame(cont, bg="#24102b")
        dias_frame.pack(fill="x", pady=2)
        self.dias_vars = [tk.BooleanVar() for _ in range(7)]
        for i, dia in enumerate(["LUN","MAR","MIE","JUE","VIE","SAB","DOM"]):
            day_toggle(dias_frame, dia, self.dias_vars[i]).pack(side="left", padx=3)
        mant_frame = tk.Frame(cont, bg="#24102b")
        mant_frame.pack(fill="x", pady=2)
        info_label(mant_frame, "Mantener").pack(side="left")
        self.mantener_chk = tk.BooleanVar()
        tk.Checkbutton(mant_frame, variable=self.mantener_chk, bg="#24102b", selectcolor="#660080").pack(side="left")
        alarma_frame = tk.Frame(cont, bg="#24102b")
        alarma_frame.pack(fill="x", pady=2)
        info_label(alarma_frame, "Alarma").pack(side="left")
        self.alarma_chk = tk.BooleanVar()
        tk.Checkbutton(alarma_frame, variable=self.alarma_chk, bg="#24102b", selectcolor="#660080").pack(side="left")
        info_label(cont, "Sonido").pack(anchor="w")
        self.sonido_var = tk.StringVar(value="JHON CENA SATURED")
        ttk.Combobox(cont, textvariable=self.sonido_var, values=["JHON CENA SATURED", "Otro sonido"]).pack(fill="x", pady=2)
        # Botones
        btn_frame = tk.Frame(self, bg="#24102b")
        btn_frame.pack(fill="x", pady=10)
        colored_button(btn_frame, "Crear", master.crear_recordatorio, size=14).pack(side="left", padx=10, ipadx=10, ipady=5)
        colored_button(btn_frame, "Volver", lambda: master.cambiar_pantalla("PrincipalScreen"), size=14).pack(side="left", padx=10, ipadx=10, ipady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()
