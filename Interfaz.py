import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont, messagebox, simpledialog
import os
import hashlib

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
        header(self, title="MediReminder", subtitle="Organiza tus tareas y recordatorios").pack(fill="x")

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
        tk.Label(usuario_card, text="Usuario", font=("Segoe UI", 16, "bold"), fg=TEXT, bg=CARD).pack(pady=8)
        tk.Label(usuario_card, text="Revisa y marca tus tareas completadas", font=("Segoe UI", 11), fg=MUTED, bg=CARD).pack(pady=(0,8))
        colored_button(usuario_card, "Ir a mis recordatorios", lambda: master.cambiar_pantalla("UsuarioScreen"), icon="🧑").pack(pady=6)

        admin_card = tk.Frame(cards_wrap, bg=CARD, bd=0, relief="flat", highlightbackground=SHADOW, highlightthickness=1)
        admin_card.pack(side="left", padx=20, ipadx=14, ipady=14)
        icon_admin = tk.Label(admin_card, text="⚙️", bg=CARD, font=("Segoe UI", 30))
        icon_admin.pack(pady=(8, 0))
        tk.Label(admin_card, text="Administrador", font=("Segoe UI", 16, "bold"), fg=TEXT, bg=CARD).pack(pady=8)
        tk.Label(admin_card, text="Añade, edita o elimina recordatorios", font=("Segoe UI", 11), fg=MUTED, bg=CARD).pack(pady=(0,8))
        colored_button(admin_card, "Panel admin", lambda m=master: m.mostrar_administrador(), icon="🛠️").pack(pady=6)

        # Footer (small)
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

class UsuarioScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        self.controlador = controlador
        header(self, title="Usuario", subtitle="Recordatorios pendientes").pack(fill="x")
        # Tarjeta principal
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        # AREA: scrollable container for user reminders so items never overlap action buttons
        top_area = tk.Frame(card, bg="#fff")
        top_area.pack(expand=True, fill="both", pady=10)

        self.scroll_canvas = tk.Canvas(top_area, bg="#fff", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        vscroll = tk.Scrollbar(top_area, orient="vertical", command=self.scroll_canvas.yview)
        vscroll.pack(side="right", fill="y")
        self.scroll_canvas.configure(yscrollcommand=vscroll.set)

        # inner frame that holds all reminder widgets
        self.usuario_cont = tk.Frame(self.scroll_canvas, bg="#fff")
        self.scroll_canvas.create_window((0, 0), window=self.usuario_cont, anchor="nw")

        # helper to keep the scrollregion updated
        def _on_usuario_configure(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        self.usuario_cont.bind("<Configure>", _on_usuario_configure)
        # mouse wheel support on Windows
        self.scroll_canvas.bind_all("<MouseWheel>", lambda e: self.scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
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
        # Muestra tareas no eliminadas y no completadas para hoy y próximos 7 días
        if self.controlador:
            from datetime import datetime, timedelta
            hoy = datetime.today().date()
            limite = hoy + timedelta(days=7)
            pendientes = []
            for r in self.controlador.modelo.obtener_pendientes():
                fecha_txt = r.get('fecha')
                if not fecha_txt:
                    continue
                try:
                    fecha_ev = datetime.strptime(fecha_txt, "%Y-%m-%d").date()
                except Exception:
                    continue
                if hoy <= fecha_ev <= limite:
                    pendientes.append(r)
            # Limpiar
            for widget in self.usuario_cont.winfo_children():
                widget.destroy()
            self.check_vars = []
            self.id_map = []
            # Split into two groups: next 24 hours and after
            from datetime import datetime, timedelta
            now = datetime.now()
            next_24h = []
            after = []
            for r in pendientes:
                fecha_txt = r.get('fecha')
                hora_txt = r.get('hora', '00:00') or '00:00'
                try:
                    # build a datetime for the event (date + time)
                    fecha_dt = datetime.strptime(fecha_txt + ' ' + hora_txt, "%Y-%m-%d %H:%M")
                except Exception:
                    # fallback: midnight of the day
                    try:
                        fecha_dt = datetime.strptime(fecha_txt + ' 00:00', "%Y-%m-%d %H:%M")
                    except Exception:
                        fecha_dt = None

                if fecha_dt:
                    if now <= fecha_dt <= now + timedelta(hours=24):
                        next_24h.append(r)
                    else:
                        after.append(r)
                else:
                    after.append(r)

            # clear previous content
            for widget in self.usuario_cont.winfo_children():
                widget.destroy()

            def _render_list(title, items):
                header = tk.Frame(self.usuario_cont, bg=CARD)
                header.pack(fill="x", padx=8, pady=(8, 2))
                tk.Label(header, text=title, fg=TEXT, bg=CARD, font=("Segoe UI", 12, "bold")).pack(anchor="w")
                if not items:
                    no_box = tk.Frame(self.usuario_cont, bg=CARD)
                    no_box.pack(fill="x", padx=8, pady=(2, 8))
                    tk.Label(no_box, text="No hay recordatorios.", fg=MUTED, bg=CARD, font=("Segoe UI", 10)).pack(anchor="w", padx=6, pady=6)
                    return
                for r in items:
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

            # Render both lists
            _render_list("Próximas 24 horas", next_24h)
            _render_list("Más adelante", after)

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
        # --- Icono de cuenta en la esquina superior derecha ---
        cuenta_btn = tk.Button(self, text="👤", bg=BG, fg=PRIMARY, font=("Segoe UI", 16), bd=0, relief="flat", cursor="hand2")
        cuenta_btn.place(relx=0.96, rely=0.03, anchor="ne")
        def borrar_cuenta():
            from tkinter import messagebox
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            pass_path = os.path.join(base_dir, 'admin_pass.txt')
            if messagebox.askyesno("Borrar cuenta", "¿Borrar la cuenta?."):
                try:
                    if os.path.exists(pass_path):
                        os.remove(pass_path)
                        messagebox.showinfo("Cuenta borrada", "La cuenta ha sido borrada :).")
                    else:
                        messagebox.showinfo("Sin contraseña", "No hay cuenta guardada actualmente.")
                except Exception:
                    messagebox.showerror("Error", "No se pudo borrar la cuenta.")
        cuenta_btn.config(command=borrar_cuenta)
        # --- Resto de tu código existente ---
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        btn_frame = tk.Frame(card, bg="#fff")
        btn_frame.pack(pady=30)
        colored_button(btn_frame, "Tareas realizadas", lambda: master.cambiar_pantalla("RealizadasScreen", anterior="PrincipalScreen"), size=20, icon="✅").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Crear Recordatorio", controlador.on_crear_evento, size=20, icon="➕").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Modificar Recordatorio", lambda: master.mostrar_lista("modificar"), size=20, icon="✏️").pack(fill="x", pady=10, ipadx=10, ipady=10)
        colored_button(btn_frame, "Inicio", lambda: master.cambiar_pantalla("InicioScreen"), size=16, icon="🔙").pack(fill="x", pady=10, ipadx=10, ipady=7)
        tk.Label(self, text="Hecho con ❤️ por tu equipo", font=("Segoe UI", 10), fg=MUTED, bg=BG).pack(side="bottom", pady=18)

class ListaRecordatoriosScreen(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=BG)
        self.controlador = controlador
        header(self, title="Lista de recordatorios", subtitle="Selecciona uno para editar o eliminar").pack(fill="x")
        card = tk.Frame(self, bg="#fff", bd=0, relief="ridge", highlightbackground="#e0e0e0", highlightthickness=2)
        card.pack(expand=True, fill="both", padx=40, pady=10)
        # Scrollable list area to hold reminders (prevents overflow when many items exist)
        lista_wrap = tk.Frame(card, bg="#fff")
        lista_wrap.pack(expand=True, fill="both", pady=10, padx=6)

        self.lista_canvas = tk.Canvas(lista_wrap, bg="#fff", highlightthickness=0)
        self.lista_canvas.pack(side="left", fill="both", expand=True)
        vscroll = tk.Scrollbar(lista_wrap, orient="vertical", command=self.lista_canvas.yview)
        vscroll.pack(side="right", fill="y")
        self.lista_canvas.configure(yscrollcommand=vscroll.set)

        self.contenedor_lista = tk.Frame(self.lista_canvas, bg="#fff")
        self.lista_canvas.create_window((0, 0), window=self.contenedor_lista, anchor="nw")

        def _on_lista_config(e):
            self.lista_canvas.configure(scrollregion=self.lista_canvas.bbox("all"))

        self.contenedor_lista.bind('<Configure>', _on_lista_config)
        self.lista_canvas.bind_all('<MouseWheel>', lambda e: self.lista_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
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

        if not eventos_mes:
            empty = tk.Frame(self.contenedor_lista, bg=CARD)
            empty.pack(fill='both', expand=True, padx=8, pady=6)
            tk.Label(empty, text="No hay recordatorios futuros.", fg=MUTED, bg=CARD, font=("Segoe UI", 11)).pack(padx=8, pady=16)
            return

        for r in eventos_mes:
            # Card-like row
            row = tk.Frame(self.contenedor_lista, bg=CARD, bd=0, highlightbackground=SHADOW, highlightthickness=1)
            row.pack(fill="x", padx=8, pady=6, ipadx=6, ipady=6)

            # left: tiny color square for important items
            color = ACCENT if r.get('importante') else SHADOW
            icon_box = tk.Frame(row, bg=color, width=10, height=10)
            icon_box.pack(side='left', padx=(8,12), pady=6)

            # center: main text
            txt = tk.Frame(row, bg=CARD)
            txt.pack(side='left', fill='x', expand=True)
            title = r.get('titulo','')
            id_lbl = f"[{r.get('id')}] "
            tk.Label(txt, text=id_lbl + title, fg=TEXT, bg=CARD, font=("Segoe UI", 11, "bold")).pack(anchor='w')
            tk.Label(txt, text=f"Fecha: {r.get('fecha','')}   Hora: {r.get('hora','')}", fg=MUTED, bg=CARD, font=("Segoe UI", 10)).pack(anchor='w')

            # right: actions — edit (double-click) and delete button
            actions = tk.Frame(row, bg=CARD)
            actions.pack(side='right', padx=8)

            # small edit hint
            edit_btn = ttk.Button(actions, text='✏️', command=lambda rec=r: self.abrir_edicion_recordatorio(rec), width=3)
            edit_btn.pack(side='right', padx=(6,0))

            # delete (trash) — use a red button for clarity
            def _make_delete(rec_item):
                def _del():
                    from tkinter import messagebox as _mb
                    if _mb.askyesno("Eliminar recordatorio", f"¿Eliminar '{rec_item.get('titulo')}' (id {rec_item.get('id')})? "):
                        try:
                            self.controlador.eliminar_recordatorio(rec_item.get('id'))
                        except Exception:
                            _mb.showerror("Error", "No se pudo eliminar el recordatorio")
                        else:
                            _mb.showinfo("Eliminado", "Recordatorio eliminado")
                            if hasattr(self, 'actualizar'):
                                self.actualizar()
                return _del

            del_btn = tk.Button(actions, text='🗑️', command=_make_delete(r), bg='#f44336', fg='white', relief='flat')
            del_btn.pack(side='right', padx=(0,6))

            # interaction: double-click anywhere on row opens edit
            row.bind('<Double-Button-1>', lambda e, rec=r: self.abrir_edicion_recordatorio(rec))
            for child in row.winfo_children():
                child.bind('<Double-Button-1>', lambda e, rec=r: self.abrir_edicion_recordatorio(rec))

    def abrir_edicion_recordatorio(self, rec):
        import tkinter as tk
        from tkinter import ttk, messagebox

        # Modal dialog for editing a reminder — improved layout and usability
        top = tk.Toplevel(self)
        top.title("Editar recordatorio")
        top.geometry("520x620")
        top.configure(bg=BG)
        top.transient(self)
        top.grab_set()
        # --- Campos (mejor diseño con grid) ---
        def info_label(parent, text, size=11):
            return tk.Label(parent, text=text, fg=MUTED, bg="#fff", anchor="w", font=("Segoe UI", size))

        cont = tk.Frame(top, bg="#fff", bd=1, relief="flat")
        cont.pack(expand=True, fill="both", padx=16, pady=12)

        # Title header
        header_frame = tk.Frame(cont, bg="#fff")
        header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(6, 12))
        tk.Label(header_frame, text="Editar recordatorio", font=("Segoe UI", 14, "bold"), fg=PRIMARY, bg="#fff").pack(anchor="w")
        tk.Label(header_frame, text="Revisa y edita los campos, luego guarda o cancela.", font=("Segoe UI", 10), fg=MUTED, bg="#fff").pack(anchor="w")

        # Left column labels, right column inputs
        info_label(cont, "Título").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        titulo_input = ttk.Entry(cont)
        titulo_input.grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=6)
        titulo_input.insert(0, rec.get("titulo", ""))

        info_label(cont, "Fecha").grid(row=2, column=0, sticky="w", padx=8, pady=6)
        fecha = rec.get("fecha", "")
        label_fecha = tk.Label(cont, text=f"{fecha}", fg=TEXT, bg="#fff", font=("Segoe UI", 11))
        label_fecha.grid(row=2, column=1, sticky="w", padx=8, pady=6)

        info_label(cont, "Hora (HH:MM)").grid(row=3, column=0, sticky="w", padx=8, pady=6)
        hora_input = ttk.Entry(cont)
        hora_input.grid(row=3, column=1, sticky="w", padx=8, pady=6)
        hora_input.insert(0, rec.get("hora", ""))

        info_label(cont, "Repetir").grid(row=4, column=0, sticky="w", padx=8, pady=6)
        repetir_var = tk.StringVar(value=rec.get("repetir", "No repetir"))
        repetir_combo = ttk.Combobox(cont, textvariable=repetir_var, values=["No repetir","Diariamente","Semanalmente","Mensualmente"])
        repetir_combo.grid(row=4, column=1, sticky="w", padx=8, pady=6)

        # Row for important/mantener/alarma checkboxes
        chk_frame = tk.Frame(cont, bg="#fff")
        chk_frame.grid(row=5, column=0, columnspan=3, sticky="w", padx=8, pady=6)
        importante_chk = tk.BooleanVar(value=rec.get("importante", False))
        tk.Checkbutton(chk_frame, text="Importante", variable=importante_chk, bg="#fff", selectcolor=ACCENT, font=("Segoe UI", 10)).pack(side="left", padx=(0,10))
        mantener_chk = tk.BooleanVar(value=rec.get("mantener", False))
        tk.Checkbutton(chk_frame, text="Mantener", variable=mantener_chk, bg="#fff", selectcolor=ACCENT, font=("Segoe UI", 10)).pack(side="left", padx=(0,10))
        alarma_chk = tk.BooleanVar(value=rec.get("alarma", False))
        tk.Checkbutton(chk_frame, text="Alarma", variable=alarma_chk, bg="#fff", selectcolor=ACCENT, font=("Segoe UI", 10)).pack(side="left")

        # Days of week - clearer layout with a labeled frame
        info_label(cont, "Días de recordatorio").grid(row=6, column=0, sticky="nw", padx=8, pady=6)
        dias_frame = tk.Frame(cont, bg="#fff")
        dias_frame.grid(row=6, column=1, columnspan=2, sticky="w", padx=8, pady=6)
        dias_vars = [tk.BooleanVar(value=False) for _ in range(7)]
        for i, dia in enumerate(["LUN","MAR","MIE","JUE","VIE","SAB","DOM"]):
            dias_vars[i].set(dia in rec.get("dias", []))
            cb = tk.Checkbutton(dias_frame, text=dia, variable=dias_vars[i], fg=PRIMARY, bg="#fff", selectcolor=SHADOW, font=("Segoe UI", 10, "bold"))
            cb.grid(row=0, column=i, padx=4)

        info_label(cont, "Sonido").grid(row=7, column=0, sticky="w", padx=8, pady=6)
        sonido_var = tk.StringVar(value=rec.get("sonido", "JHON CENA SATURED"))
        sonido_combo = ttk.Combobox(cont, textvariable=sonido_var, values=["JHON CENA SATURED", "Otro sonido"])
        sonido_combo.grid(row=7, column=1, sticky="w", padx=8, pady=6)

        # Make grid expand nicely
        cont.columnconfigure(1, weight=1)
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
            # Validate time format HH:MM
            import re
            if not re.match(r"^\d{1,2}:\d{2}$", hora):
                messagebox.showerror("Hora inválida", "Usa el formato HH:MM, por ejemplo 09:00 o 18:30")
                return

            self.controlador.modelo.actualizar_recordatorio(rec.get("id"), datos)

            # Registrar en historial como modificación del administrador
            self.controlador.modelo.registrar_historial(rec.get("id"), "Administrador", "modificó recordatorio")

            if hasattr(self, "actualizar"):
                self.actualizar()
            # Close modal
            top.grab_release()
            top.destroy()



        # Action buttons — placed visibly and centered
        btns = tk.Frame(top, bg=BG)
        btns.pack(pady=14)
        save_btn = ttk.Button(btns, text="💾 Guardar cambios", command=guardar)
        save_btn.pack(side="left", padx=10, ipadx=10, ipady=8)
        cancel_btn = ttk.Button(btns, text="✖️ Cancelar", command=lambda: (top.grab_release(), top.destroy()))
        cancel_btn.pack(side="left", padx=10, ipadx=10, ipady=8)

        # Focus and keyboard friendliness
        titulo_input.focus_set()
        top.bind('<Return>', lambda e: guardar())
        top.bind('<Escape>', lambda e: (top.grab_release(), top.destroy()))

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
        # Asegura que haya una fecha por defecto (hoy) para crear desde la UI sin pasar por calendario
        from datetime import datetime
        self.fecha_seleccionada = datetime.today().strftime('%Y-%m-%d')
        # Mostrar la fecha por defecto en la interfaz
        if not hasattr(self, 'label_fecha'):
            self.label_fecha = tk.Label(self, text=f"Fecha seleccionada: {self.fecha_seleccionada}", fg=PRIMARY, bg="#fff", font=("Segoe UI", 12, "bold"))
            self.label_fecha.pack(pady=5)

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

    # Actualiza en el modelo
    self.controlador.modelo.actualizar_recordatorio(rec_id, datos)

    # Registrar en historial como modificación del administrador
    self.controlador.modelo.registrar_historial(rec_id, "Administrador", "modificó recordatorio")

    # Volver a la lista
    self.cambiar_pantalla("ListaRecordatoriosScreen", anterior="PrincipalScreen")


class App(tk.Tk):
    def __init__(self, controlador=None):
        super().__init__()
        self.title("Recordatorios")
        self.geometry("650x750")
        self.configure(bg=BG)
        self.controlador = controlador
        self.frames = {}
        # pantalla_anterior: the previous screen used for navigation
        self.pantalla_anterior = None
        # current_screen: name of the currently visible screen
        self.current_screen = None
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
        # keep track of the current screen so other logic can behave based on origin
        self.current_screen = nombre
        # Sincroniza el rol según la pantalla
        if self.controlador:
            if nombre == "PrincipalScreen":
                self.controlador.set_rol("Administrador")
            elif nombre == "UsuarioScreen":
                self.controlador.set_rol("Usuario")
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
        # Prefer current screen as the origin - ensures we know where the user came from
        anterior = self.current_screen or self.pantalla_anterior or "UsuarioScreen"
        self.cambiar_pantalla("RecordatorioScreen", anterior=anterior)
        recordatorio_screen = self.frames.get("RecordatorioScreen")
        if recordatorio_screen and hasattr(recordatorio_screen, "set_fecha"):
            recordatorio_screen.set_fecha(fecha_str)
            # Asegura que no haya id_edicion previa
            recordatorio_screen.id_edicion = None

    def mostrar_administrador(self):
        """Ask the user for admin access. If no password exists, prompt to create one.

        Passwords are stored as a SHA256 hash in a file named `admin_pass.txt`
        in the same directory as this module.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pass_path = os.path.join(base_dir, 'admin_pass.txt')

        def _open_admin():
            self.cambiar_pantalla('PrincipalScreen')

        # If a password exists, request it
        if os.path.exists(pass_path) and os.path.getsize(pass_path) > 0:
            try:
                with open(pass_path, 'r', encoding='utf-8') as f:
                    stored = f.read().strip()
            except Exception:
                stored = ''

            pwd = simpledialog.askstring("Acceso Administrador", "Introduce la contraseña:", show="*", parent=self)
            if pwd is None:
                return
            if hashlib.sha256(pwd.encode('utf-8')).hexdigest() == stored:
                _open_admin()
            else:
                messagebox.showerror("Acceso denegado", "Contraseña incorrecta.", parent=self)
            return

        # No password set — ask user to create one
        top = tk.Toplevel(self)
        top.title("Crear contraseña administrador")
        top.transient(self)
        top.grab_set()
        top.configure(bg=BG)
        tk.Label(top, text="No hay contraseña de administrador configurada.", bg=BG, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(padx=12, pady=(12, 6))
        tk.Label(top, text="Crea una contraseña para el acceso de administrador:", bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(padx=12, pady=(0, 12))

        frm = tk.Frame(top, bg=BG)
        frm.pack(fill='x', padx=12)
        tk.Label(frm, text="Contraseña:", bg=BG, fg=TEXT).pack(anchor='w')
        pw1 = tk.StringVar()
        e1 = ttk.Entry(frm, textvariable=pw1, show='*')
        e1.pack(fill='x', pady=6)
        tk.Label(frm, text="Confirmar contraseña:", bg=BG, fg=TEXT).pack(anchor='w')
        pw2 = tk.StringVar()
        e2 = ttk.Entry(frm, textvariable=pw2, show='*')
        e2.pack(fill='x', pady=6)

        def crear_pwd():
            v1 = pw1.get().strip()
            v2 = pw2.get().strip()
            if not v1:
                messagebox.showerror("Error", "La contraseña no puede estar vacía.", parent=top)
                return
            if v1 != v2:
                messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=top)
                return
            if len(v1) < 4:
                messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.", parent=top)
                return
            try:
                with open(pass_path, 'w', encoding='utf-8') as f:
                    f.write(hashlib.sha256(v1.encode('utf-8')).hexdigest())
            except Exception:
                messagebox.showerror("Error", "No se pudo guardar la contraseña.", parent=top)
                return
            messagebox.showinfo("Listo", "Contraseña guardada. Ahora podrás acceder como administrador.", parent=top)
            top.grab_release()
            top.destroy()

        btns = tk.Frame(top, bg=BG)
        btns.pack(pady=10)
        ttk.Button(btns, text="Crear contraseña", command=crear_pwd).pack(side='left', padx=8)
        ttk.Button(btns, text="Cancelar", command=lambda: (top.grab_release(), top.destroy())).pack(side='left', padx=8)

# Añade el método a la clase App
setattr(App, "guardar_cambios_recordatorio", guardar_cambios_recordatorio)
