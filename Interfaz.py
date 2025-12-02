import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

# Medisafe-inspired palette
BG = "#f4f8fb"          # app background (very light)
PRIMARY = "#2b87f0"     # primary blue-ish
ACCENT = "#14c1a3"      # accent (teal)
CARD = "#ffffff"         # card background
TEXT = "#0f1722"        # primary text
MUTED = "#6b7280"       # muted text
SHADOW = "#e6eefc"      # subtle shadow toner

# Widgets personalizados
def dark_label(parent, text, size=14, bold=False):
    font = ("Segoe UI", size, "bold" if bold else "normal")
    return tk.Label(parent, text=text, fg=TEXT, bg=BG, font=font)

def info_label(parent, text, size=12):
    return tk.Label(parent, text=text, fg=MUTED, bg=BG, anchor="w", font=("Segoe UI", size))

def colored_button(parent, text, command=None, size=14, icon=None):
    btn_text = f"{icon} {text}" if icon else text
    return ttk.Button(parent, text=btn_text, command=command, style="TButton")

def day_toggle(parent, text, var):
    return tk.Checkbutton(parent, text=text, fg=PRIMARY, bg=BG, selectcolor=SHADOW, variable=var, font=("Segoe UI", 10, "bold"))


def header(parent, title=None, subtitle=None):
    """Create a Medisafe-like header with a logo and optional subtitle."""
    hdr = tk.Frame(parent, bg=BG)
    top = tk.Frame(hdr, bg=BG)
    top.pack(fill="x", padx=24, pady=8)
    left = tk.Frame(top, bg=BG)
    left.pack(side="left", anchor="w")
    logo = tk.Label(left, text="💊", font=("Segoe UI", 20), bg=BG)
    logo.pack(side="left")
    txt_frame = tk.Frame(left, bg=BG)
    txt_frame.pack(side="left", padx=8)
    tk.Label(txt_frame, text=title or "MediReminder", font=("Segoe UI", 18, "bold"), fg=PRIMARY, bg=BG).pack(anchor="w")
    if subtitle:
        tk.Label(txt_frame, text=subtitle, font=("Segoe UI", 11), fg=MUTED, bg=BG).pack(anchor="w")
    # right: small profile circle
    right = tk.Frame(top, bg=BG)
    right.pack(side="right", anchor="e")
    avatar = tk.Label(right, text="😊", bg=BG, font=("Segoe UI", 14))
    avatar.pack()
    return hdr

# Pantallas
class InicioScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        # Header
        header(self, title="MediReminder", subtitle="Organiza tus medicamentos y recordatorios").pack(fill="x")

        # Tarjetas y resumen — estilo Medisafe: tarjeta resumen + acciones
        card_frame = tk.Frame(self, bg=BG)
        card_frame.pack(pady=50)

        # resumen 'Hoy' arriba
        today_card = tk.Frame(card_frame, bg=CARD, bd=0, relief="flat", highlightbackground=SHADOW, highlightthickness=1)
        today_card.pack(fill="x", padx=40, pady=(10, 24), ipadx=12, ipady=12)
        t_left = tk.Frame(today_card, bg=CARD)
        t_left.pack(side="left")
        tk.Label(t_left, text="Hoy", font=("Segoe UI", 14, "bold"), fg=TEXT, bg=CARD).pack(anchor="w")
        # Cambia este label para que sea accesible desde el controlador
        self.label_resumen_pendientes = tk.Label(t_left, text="0 recordatorios por resolver", font=("Segoe UI", 11), fg=MUTED, bg=CARD)
        self.label_resumen_pendientes.pack(anchor="w")
        # quick actions to the right
        t_right = tk.Frame(today_card, bg=CARD)
        t_right.pack(side="right")
        colored_button(t_right, "Ver hoy", lambda: master.cambiar_pantalla("UsuarioScreen"), icon="📅").pack()

        # acción principal: dos tarjetas grandes
        cards_wrap = tk.Frame(card_frame, bg=BG)
        cards_wrap.pack(pady=4)

        usuario_card = tk.Frame(cards_wrap, bg=CARD, bd=0, relief="flat", highlightbackground=SHADOW, highlightthickness=1)
        usuario_card.pack(side="left", padx=20, ipadx=14, ipady=14)
        icon_usr = tk.Label(usuario_card, text="🧑‍⚕️", bg=CARD, font=("Segoe UI", 30))
        icon_usr.pack(pady=(8, 0))
        tk.Label(usuario_card, text="Mi medicación", font=("Segoe UI", 16, "bold"), fg=TEXT, bg=CARD).pack(pady=8)
        tk.Label(usuario_card, text="Revisa y marca tus medicamentos tomados", font=("Segoe UI", 11), fg=MUTED, bg=CARD).pack(pady=(0,8))
        colored_button(usuario_card, "Ir a mis recordatorios", lambda: master.cambiar_pantalla("UsuarioScreen"), icon="🧑").pack(pady=6)

        admin_card = tk.Frame(cards_wrap, bg=CARD, bd=0, relief="flat", highlightbackground=SHADOW, highlightthickness=1)
        admin_card.pack(side="left", padx=20, ipadx=14, ipady=14)
        icon_admin = tk.Label(admin_card, text="⚙️", bg=CARD, font=("Segoe UI", 30))
        icon_admin.pack(pady=(8, 0))
        tk.Label(admin_card, text="Administrador", font=("Segoe UI", 16, "bold"), fg=TEXT, bg=CARD).pack(pady=8)
        tk.Label(admin_card, text="Añade, edita o elimina recordatorios", font=("Segoe UI", 11), fg=MUTED, bg=CARD).pack(pady=(0,8))
        colored_button(admin_card, "Panel admin", lambda: master.cambiar_pantalla("PrincipalScreen"), icon="🛠️").pack(pady=6)

        # Footer (small)
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

class UsuarioScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        self.controlador = controlador
        header(self, title="Mi medicación", subtitle="Recordatorios pendientes").pack(fill="x")
        # Tarjeta principal
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        self.usuario_cont = tk.Frame(card, bg="#fff")
        self.usuario_cont.pack(expand=True, fill="both", pady=10)
        # Botones de acciones
        btns = tk.Frame(card, bg="#fff")
        btns.pack(pady=10)
        colored_button(btns, "Crear evento", controlador.on_crear_evento, size=14, icon="➕").pack(side="left", padx=12, ipadx=10, ipady=5)
        colored_button(btns, "Eliminar evento", self.eliminar_evento, size=14, icon="🗑️").pack(side="left", padx=12, ipadx=10, ipady=5)
        colored_button(btns, "Ver realizadas", lambda: master.cambiar_pantalla("RealizadasScreen", anterior="UsuarioScreen"), size=14, icon="✅").pack(side="left", padx=12, ipadx=10, ipady=5)
        colored_button(card, "Volver", lambda: master.cambiar_pantalla("InicioScreen"), size=14, icon="🔙").pack(pady=8, ipadx=10, ipady=5)
        # Floating action button — estilo Medisafe para añadir rápidamente
        # fab = tk.Button(self, text="+", bg=PRIMARY, fg="white", font=("Segoe UI", 20, "bold"), bd=0, relief="flat", command=controlador.on_crear_evento)
        # fab.configure(activebackground="#5aa0ff")
        # fab.place(relx=0.92, rely=0.84, anchor="center")
        # Variable para saber qué tarea está seleccionada para eliminar
        self.tarea_seleccionada = tk.IntVar(value=0)
        # Footer
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

    def actualizar(self):
        # Muestra tareas no eliminadas y no completadas, SOLO para hoy, mostrando fecha y hora
        if self.controlador:
            from datetime import datetime
            hoy = datetime.today().date()
            pendientes = [
                r for r in self.controlador.modelo.obtener_pendientes()
                if r.get('fecha') == hoy.strftime("%Y-%m-%d")
            ]
            # Limpiar
            for widget in self.usuario_cont.winfo_children():
                widget.destroy()
            self.check_vars = []
            self.id_map = []
            for r in pendientes:
                var = tk.BooleanVar(value=False)
                frame = tk.Frame(self.usuario_cont, bg=CARD, bd=0, highlightbackground=SHADOW, highlightthickness=1)
                frame.pack(fill="x", padx=8, pady=6)
                chk = tk.Checkbutton(frame, variable=var, bg=CARD, selectcolor=ACCENT,
                                     command=lambda rid=r['id'], v=var: self.marcar_completado(rid, v))
                chk.pack(side="left", padx=8, pady=8)
                # title + date + time
                text_frame = tk.Frame(frame, bg=CARD)
                text_frame.pack(side="left", fill="x", expand=True, padx=6, pady=8)
                tk.Label(text_frame, text=f"{r.get('titulo','')}", fg=TEXT, bg=CARD, font=("Segoe UI", 11, "bold")).pack(anchor="w")
                fecha = r.get('fecha', '')
                hora = r.get('hora', '')
                tk.Label(text_frame, text=f"Fecha: {fecha}   Hora: {hora}", fg=MUTED, bg=CARD, font=("Segoe UI", 10)).pack(anchor="w")
                # Radio para seleccionar para eliminar
                radio = tk.Radiobutton(frame, variable=self.tarea_seleccionada, value=r['id'], bg=CARD)
                radio.pack(side="right")
                self.check_vars.append(var)
                self.id_map.append(r['id'])

    def marcar_completado(self, rec_id, var):
        if var.get():
            self.controlador.marcar_completado(rec_id)

    def eliminar_evento(self):
        rec_id = self.tarea_seleccionada.get()
        if rec_id:
            self.controlador.eliminar_recordatorio(rec_id)
            self.tarea_seleccionada.set(0)

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

class PrincipalScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        header(self, title="Administrador", subtitle="Gestiona tus recordatorios").pack(fill="x")
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        btn_frame = tk.Frame(card, bg="#fff")
        btn_frame.pack(pady=30)
        colored_button(btn_frame, "Tareas realizadas", lambda: master.cambiar_pantalla("RealizadasScreen", anterior="PrincipalScreen"), size=20, icon="✅").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Crear Recordatorio", controlador.on_crear_evento, size=20, icon="➕").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Eliminar Recordatorio", lambda: master.mostrar_lista("eliminar"), size=20, icon="🗑️").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Modificar Recordatorio", lambda: master.mostrar_lista("modificar"), size=20, icon="✏️").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Inicio", lambda: master.cambiar_pantalla("InicioScreen"), size=16, icon="🔙").pack(fill="x", pady=10, ipadx=10, ipady=7)
        # Floating action button for quick add
        # fab = tk.Button(self, text="+", bg=PRIMARY, fg="white", font=("Segoe UI", 20, "bold"), bd=0, relief="flat", command=controlador.on_crear_evento)
        # fab.configure(activebackground="#5aa0ff")
        # fab.place(relx=0.92, rely=0.86, anchor="center")

        # Footer
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

class ListaRecordatoriosScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        self.controlador = controlador
        header(self, title="Lista de recordatorios", subtitle="Selecciona uno para editar o eliminar").pack(fill="x")
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        self.contenedor_lista = tk.Frame(card, bg="#fff")
        self.contenedor_lista.pack(expand=True, fill="both", pady=10)
        # Botón volver funcional
        colored_button(card, "Volver", self.volver_a_principal, size=14, icon="🔙").pack(pady=10, ipadx=10, ipady=5)
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

    def volver_a_principal(self):
        # Siempre vuelve a la pantalla principal
        self.master.cambiar_pantalla("PrincipalScreen")

    def actualizar(self):
        from datetime import datetime
        hoy = datetime.today().date()
        datos = self.controlador.modelo.cargar_todos()
        eventos_mes = []
        for r in datos:
            try:
                fecha_ev = datetime.strptime(r.get('fecha', ''), "%Y-%m-%d").date()
                if fecha_ev >= hoy and not r.get('eliminado'):
                    eventos_mes.append(r)
            except Exception:
                continue
        for widget in self.contenedor_lista.winfo_children():
            widget.destroy()
        for r in eventos_mes:
            texto = f"[{r.get('id')}] {r.get('titulo','')} - Fecha: {r.get('fecha','')} Hora: {r.get('hora','')}"
            lbl = tk.Label(self.contenedor_lista, text=texto, fg=TEXT, bg=CARD, anchor="w", font=("Segoe UI", 11))
            lbl.pack(fill="x", padx=8, pady=2)
            # Doble click para editar
            lbl.bind("<Double-Button-1>", lambda e, rec=r: self.abrir_edicion_recordatorio(rec))
            # Click derecho para eliminar (marcar como eliminado)
            lbl.bind("<Button-3>", lambda e, rec=r: self.eliminar_evento_confirmar(rec))

    def abrir_edicion_recordatorio(self, rec):
        import tkinter as tk
        from tkinter import ttk, messagebox
        top = tk.Toplevel(self)
        top.title("Editar recordatorio")
        top.geometry("500x600")
        top.configure(bg=BG)
        # --- Campos ---
        def info_label(parent, text, size=12):
            return tk.Label(parent, text=text, fg=MUTED, bg=BG, anchor="w", font=("Segoe UI", size))
        cont = tk.Frame(top, bg="#fff")
        cont.pack(expand=True, fill="both", padx=16, pady=10)
        info_label(cont, "Título").pack(anchor="w")
        titulo_input = ttk.Entry(cont)
        titulo_input.pack(fill="x", pady=2)
        titulo_input.insert(0, rec.get("titulo", ""))
        info_label(cont, "Hora (HH:MM)").pack(anchor="w")
        hora_input = ttk.Entry(cont)
        hora_input.pack(fill="x", pady=2)
        hora_input.insert(0, rec.get("hora", ""))
        info_label(cont, "Repetir").pack(anchor="w")
        repetir_var = tk.StringVar(value=rec.get("repetir", "No repetir"))
        ttk.Combobox(cont, textvariable=repetir_var, values=["No repetir","Diariamente","Semanalmente","Mensualmente"]).pack(fill="x", pady=2)
        imp_frame = tk.Frame(cont, bg="#fff")
        imp_frame.pack(fill="x", pady=2)
        info_label(imp_frame, "Importante").pack(side="left")
        importante_chk = tk.BooleanVar(value=rec.get("importante", False))
        tk.Checkbutton(imp_frame, variable=importante_chk, bg=CARD, selectcolor=ACCENT).pack(side="left")
        info_label(cont, "Días de recordatorio").pack(anchor="w")
        dias_frame = tk.Frame(cont, bg="#fff")
        dias_frame.pack(fill="x", pady=2)
        dias_vars = [tk.BooleanVar(value=False) for _ in range(7)]
        for i, dia in enumerate(["LUN","MAR","MIE","JUE","VIE","SAB","DOM"]):
            dias_vars[i].set(dia in rec.get("dias", []))
            tk.Checkbutton(dias_frame, text=dia, variable=dias_vars[i], fg=PRIMARY, bg=BG, selectcolor=SHADOW, font=("Segoe UI", 10, "bold")).pack(side="left", padx=3)
        mant_frame = tk.Frame(cont, bg="#fff")
        mant_frame.pack(fill="x", pady=2)
        info_label(mant_frame, "Mantener").pack(side="left")
        mantener_chk = tk.BooleanVar(value=rec.get("mantener", False))
        tk.Checkbutton(mant_frame, variable=mantener_chk, bg=CARD, selectcolor=ACCENT).pack(side="left")
        alarma_frame = tk.Frame(cont, bg="#fff")
        alarma_frame.pack(fill="x", pady=2)
        info_label(alarma_frame, "Alarma").pack(side="left")
        alarma_chk = tk.BooleanVar(value=rec.get("alarma", False))
        tk.Checkbutton(alarma_frame, variable=alarma_chk, bg=CARD, selectcolor=ACCENT).pack(side="left")
        info_label(cont, "Sonido").pack(anchor="w")
        sonido_var = tk.StringVar(value=rec.get("sonido", "JHON CENA SATURED"))
        ttk.Combobox(cont, textvariable=sonido_var, values=["JHON CENA SATURED", "Otro sonido"]).pack(fill="x", pady=2)
        # Fecha
        fecha = rec.get("fecha", "")
        label_fecha = tk.Label(cont, text=f"Fecha seleccionada: {fecha}", fg=PRIMARY, bg="#fff", font=("Segoe UI", 12, "bold"))
        label_fecha.pack(pady=5)
        # --- Botones ---
        def guardar():
            titulo = titulo_input.get().strip()
            hora = hora_input.get().strip()
            repetir = repetir_var.get()
            importante = importante_chk.get()
            dias = [dia for i, dia in enumerate(["LUN","MAR","MIE","JUE","VIE","SAB","DOM"]) if dias_vars[i].get()]
            mantener = mantener_chk.get()
            alarma = alarma_chk.get()
            sonido = sonido_var.get()
            if not titulo or not hora or not fecha:
                messagebox.showerror("Error", "Debes completar título, hora y fecha.")
                return
            datos = {
                "titulo": titulo,
                "hora": hora,
                "repetir": repetir,
                "importante": importante,
                "dias": dias,
                "mantener": mantener,
                "alarma": alarma,
                "sonido": sonido,
                "fecha": fecha,
                "id": rec.get("id")
            }
            self.controlador.modelo.actualizar_recordatorio(rec.get("id"), datos)
            if hasattr(self, "actualizar"):
                self.actualizar()
            top.destroy()
        btns = tk.Frame(top, bg="#fff")
        btns.pack(pady=10)
        ttk.Button(btns, text="Guardar cambios", command=guardar).pack(side="left", padx=10, ipadx=10, ipady=5)
        ttk.Button(btns, text="Cancelar", command=top.destroy).pack(side="left", padx=10, ipadx=10, ipady=5)

    def eliminar_evento_confirmar(self, rec):
        from tkinter import messagebox
        if messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar este recordatorio?"):
            self.controlador.eliminar_recordatorio(rec['id'])
            self.actualizar()

class RealizadasScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        self.controlador = controlador
        header(self, title="Tareas realizadas", subtitle="Historial de recordatorios").pack(fill="x")
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        self.contenedor_lista = tk.Frame(card, bg="#fff")
        self.contenedor_lista.pack(expand=True, fill="both", pady=10)
        colored_button(card, "Volver", lambda: master.cambiar_pantalla(master.pantalla_anterior or "PrincipalScreen"), size=14, icon="🔙").pack(pady=10, ipadx=10, ipady=5)
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

    def actualizar(self):
        # Mostrar tareas completadas (no eliminadas) y eliminadas (historial)
        datos = self.controlador.modelo.cargar_todos()
        tareas_realizadas = []
        for r in datos:
            # Mostrar tanto completados como eliminados
            if r.get('completado') or r.get('eliminado'):
                tareas_realizadas.append(r)
        for widget in self.contenedor_lista.winfo_children():
            widget.destroy()
        for r in tareas_realizadas:
            # Distintivo de eliminado o completado
            if r.get('eliminado'):
                texto = f"❌ [{r.get('id')}] {r.get('titulo','')} - Fecha: {r.get('fecha','')} Hora: {r.get('hora','')}"
                color = "#b91c1c"
                font = ("Segoe UI", 11, "bold")
            else:
                texto = f"✔️ [{r.get('id')}] {r.get('titulo','')} - Fecha: {r.get('fecha','')} Hora: {r.get('hora','')}"
                color = "#15803d"
                font = ("Segoe UI", 11)
            lbl = tk.Label(self.contenedor_lista, text=texto, fg=color, bg=CARD, anchor="w", font=font)
            lbl.pack(fill="x", padx=8, pady=2)
            lbl.bind("<Double-Button-1>", lambda e, rec=r: self.abrir_detalle_recordatorio(rec))

    def abrir_detalle_recordatorio(self, rec):
        from tkinter import messagebox
        detalles = f"Título: {rec.get('titulo')}\nFecha: {rec.get('fecha')}\nHora: {rec.get('hora')}\nRepetir: {rec.get('repetir')}\nImportante: {'Sí' if rec.get('importante') else 'No'}"
        dias = rec.get("dias", [])
        detalles += "\nDías: " + (", ".join(dias) if dias else "No aplica")
        detalles += f"\nMantener: {'Sí' if rec.get('mantener') else 'No'}"
        detalles += f"\nAlarma: {'Sí' if rec.get('alarma') else 'No'}"
        detalles += f"\nSonido: {rec.get('sonido', 'Ninguno')}"
        if rec.get('eliminado'):
            detalles += f"\nEstado: ELIMINADO"
        elif rec.get('completado'):
            detalles += f"\nEstado: COMPLETADO"
        messagebox.showinfo("Detalles del recordatorio", detalles)

# Pantalla de recordatorio (agregar/editar)
class RecordatorioScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        header(self, title="Añadir recordatorio", subtitle="Rellena los datos para crear un recordatorio").pack(fill="x")
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        cont = tk.Frame(card, bg="#fff")
        cont.pack(expand=True, fill="both", padx=16, pady=10)
        info_label(cont, "Título").pack(anchor="w")
        self.titulo_input = ttk.Entry(cont)
        self.titulo_input.pack(fill="x", pady=2)
        info_label(cont, "Hora (HH:MM)").pack(anchor="w")
        self.hora_input = ttk.Entry(cont)
        self.hora_input.insert(0, "10:05")
        self.hora_input.pack(fill="x", pady=2)
        info_label(cont, "Repetir").pack(anchor="w")
        self.repetir_var = tk.StringVar(value="No repetir")
        ttk.Combobox(cont, textvariable=self.repetir_var, values=["No repetir","Diariamente","Semanalmente","Mensualmente"]).pack(fill="x", pady=2)
        imp_frame = tk.Frame(cont, bg="#fff")
        imp_frame.pack(fill="x", pady=2)
        info_label(imp_frame, "Importante").pack(side="left")
        self.importante_chk = tk.BooleanVar()
        tk.Checkbutton(imp_frame, variable=self.importante_chk, bg=CARD, selectcolor=ACCENT).pack(side="left")
        info_label(cont, "Días de recordatorio").pack(anchor="w")
        dias_frame = tk.Frame(cont, bg="#fff")
        dias_frame.pack(fill="x", pady=2)
        self.dias_vars = [tk.BooleanVar() for _ in range(7)]
        for i, dia in enumerate(["LUN","MAR","MIE","JUE","VIE","SAB","DOM"]):
            day_toggle(dias_frame, dia, self.dias_vars[i]).pack(side="left", padx=3)
        mant_frame = tk.Frame(cont, bg="#fff")
        mant_frame.pack(fill="x", pady=2)
        info_label(mant_frame, "Mantener").pack(side="left")
        self.mantener_chk = tk.BooleanVar()
        tk.Checkbutton(mant_frame, variable=self.mantener_chk, bg=CARD, selectcolor=ACCENT).pack(side="left")
        alarma_frame = tk.Frame(cont, bg="#fff")
        alarma_frame.pack(fill="x", pady=2)
        info_label(alarma_frame, "Alarma").pack(side="left")
        self.alarma_chk = tk.BooleanVar()
        tk.Checkbutton(alarma_frame, variable=self.alarma_chk, bg=CARD, selectcolor=ACCENT).pack(side="left")
        info_label(cont, "Sonido").pack(anchor="w")
        self.sonido_var = tk.StringVar(value="JHON CENA SATURED")
        ttk.Combobox(cont, textvariable=self.sonido_var, values=["JHON CENA SATURED", "Otro sonido"]).pack(fill="x", pady=2)
        # Botones
        btn_frame = tk.Frame(card, bg="#fff")
        btn_frame.pack(fill="x", pady=10)
        self.btn_crear = colored_button(
            btn_frame,
            "Crear",
            controlador.crear_recordatorio_desde_vista,
            size=14,
            icon="✅"
        )
        self.btn_crear.pack(side="left", padx=10, ipadx=10, ipady=5)
        self.btn_volver = colored_button(
            btn_frame,
            "Volver",
            lambda: master.cambiar_pantalla(master.pantalla_anterior or "PrincipalScreen"),
            size=14,
            icon="🔙"
        )
        self.btn_volver.pack(side="left", padx=10, ipadx=10, ipady=5)
        # Footer
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=PRIMARY, bg=BG).pack(side="bottom", pady=18)
        # Inicializa id_edicion en None
        self.id_edicion = None

    def set_fecha(self, fecha_str):
        self.fecha_seleccionada = fecha_str
        # Mostrar la fecha en la interfaz si lo deseas
        if hasattr(self, "label_fecha"):
            self.label_fecha.config(text=f"Fecha seleccionada: {fecha_str}")
        else:
            self.label_fecha = tk.Label(self, text=f"Fecha seleccionada: {fecha_str}", fg=PRIMARY, bg="#fff", font=("Segoe UI", 12, "bold"))
            self.label_fecha.pack(pady=5)

def guardar_cambios_recordatorio(self, recordatorio_screen):
    # Obtiene los datos del formulario
    titulo = recordatorio_screen.titulo_input.get().strip()
    hora = recordatorio_screen.hora_input.get().strip()
    repetir = recordatorio_screen.repetir_var.get()
    importante = recordatorio_screen.importante_chk.get()
    dias = [dia for i, dia in enumerate(["LUN","MAR","MIE","JUE","VIE","SAB","DOM"]) if recordatorio_screen.dias_vars[i].get()]
    mantener = recordatorio_screen.mantener_chk.get()
    alarma = recordatorio_screen.alarma_chk.get()
    sonido = recordatorio_screen.sonido_var.get()
    fecha = getattr(recordatorio_screen, "fecha_seleccionada", None)
    rec_id = getattr(recordatorio_screen, "id_edicion", None)
    if not titulo or not hora or not fecha or not rec_id:
        from tkinter import messagebox
        messagebox.showerror("Error", "Debes completar título, hora, fecha y tener un id válido.")
        return
    datos = {
        "titulo": titulo,
        "hora": hora,
        "repetir": repetir,
        "importante": importante,
        "dias": dias,
        "mantener": mantener,
        "alarma": alarma,
        "sonido": sonido,
        "fecha": fecha,
        "id": rec_id
    }
    self.controlador.modelo.actualizar_recordatorio(rec_id, datos)
    self.cambiar_pantalla("ListaRecordatoriosScreen", anterior="PrincipalScreen")

class App(tk.Tk):
    def __init__(self, controlador=None):
        super().__init__()
        self.title("Recordatorios")
        self.geometry("650x750")
        self.configure(bg=BG)
        self.controlador = controlador
        self.frames = {}
        self.pantalla_anterior = None
        # Fuente moderna
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=12)
        self.option_add("*Font", self.default_font)
        # ttk theme
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 12), padding=8, relief="flat", background=PRIMARY, foreground="white", borderwidth=0)
        style.map("TButton",
            background=[("active", "#5aa0ff")],
            foreground=[("active", TEXT)]
        )
        style.configure("TCombobox", fieldbackground=CARD, background=CARD, foreground=TEXT)
        style.configure("TEntry", fieldbackground=CARD, background=CARD, foreground=TEXT)
        # Pasa el controlador a cada pantalla
        for F in (InicioScreen, UsuarioScreen, PrincipalScreen, RealizadasScreen, RecordatorioScreen, ListaRecordatoriosScreen):
            frame = F(self, controlador)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        self.cambiar_pantalla("InicioScreen")

    def cambiar_pantalla(self, nombre, anterior=None):
        for f in self.frames.values():
            f.place_forget()
        self.frames[nombre].place(relwidth=1, relheight=1)
        # Guarda la pantalla anterior si se pasa
        if anterior:
            self.pantalla_anterior = anterior
        # Llama a métodos de actualización si existen
        frame = self.frames[nombre]
        if hasattr(frame, "actualizar"):
            frame.actualizar()

    def leer_pendientes(self):
        if self.controlador:
            self.controlador.actualizar_pendientes_usuario()

    # Métodos de ejemplo para enlazar con botones
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

    def abrir_plantilla_agregar_evento(self, fecha_str):
        # Cambia a la pantalla de agregar recordatorio y coloca la fecha seleccionada
        # Detecta si vienes de usuario o admin
        anterior = self.pantalla_anterior or "UsuarioScreen"
        self.cambiar_pantalla("RecordatorioScreen", anterior=anterior)
        recordatorio_screen = self.frames.get("RecordatorioScreen")
        if recordatorio_screen and hasattr(recordatorio_screen, "set_fecha"):
            recordatorio_screen.set_fecha(fecha_str)
            # Asegura que no haya id_edicion previa
            recordatorio_screen.id_edicion = None

setattr(App, "guardar_cambios_recordatorio", guardar_cambios_recordatorio)
