from Modelo import MemoriaModelo
from Interfaz import App
import os

class Controlador:
    def __init__(self):
        self._asegurar_archivo_json()
        self.modelo = MemoriaModelo()
        self.vista = App(controlador=self)
        # Al iniciar, muestra los pendientes si está en UsuarioScreen
        self.actualizar_pendientes_usuario()

    def _asegurar_archivo_json(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, 'recordatorios.json')
        if not os.path.exists(data_path):
            with open(data_path, 'w', encoding='utf-8') as f:
                f.write('[]')

    # Métodos para conectar eventos de la vista con el modelo
    def leer_pendientes(self):
        self.actualizar_pendientes_usuario()

    def actualizar_pendientes_usuario(self):
        # Obtiene los recordatorios no completados y no eliminados
        pendientes = [r for r in self.modelo.cargar_todos() if not r.get('completado') and not r.get('eliminado')]
        frame = self.vista.frames.get("UsuarioScreen")
        if frame and hasattr(frame, "usuario_cont"):
            # Limpia el contenedor
            for widget in frame.usuario_cont.winfo_children():
                widget.destroy()
            # Muestra cada recordatorio pendiente
            for r in pendientes:
                texto = f"[{r.get('id')}] {r.get('titulo','')} - {r.get('hora','')}"
                import tkinter as tk
                lbl = tk.Label(frame.usuario_cont, text=texto, fg="#0f1722", bg="#ffffff", anchor="w")
                lbl.pack(fill="x", padx=8, pady=2)

        # Actualiza el contador de pendientes en la pantalla de inicio
        self.actualizar_resumen_inicio(len(pendientes))

        # También actualiza la pantalla de realizadas
        self.actualizar_realizadas()

    def actualizar_resumen_inicio(self, cantidad):
        # Actualiza el texto de "X recordatorios por resolver" en la pantalla de inicio
        frame = self.vista.frames.get("InicioScreen")
        if frame and hasattr(frame, "label_resumen_pendientes"):
            frame.label_resumen_pendientes.config(text=f"{cantidad} recordatorios por resolver")
        else:
            # Busca el label y lo crea si no existe
            import tkinter as tk
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for subwidget in widget.winfo_children():
                        if isinstance(subwidget, tk.Label) and "recordatorios por resolver" in subwidget.cget("text"):
                            subwidget.config(text=f"{cantidad} recordatorios por resolver")
                            frame.label_resumen_pendientes = subwidget
                            return

    def actualizar_realizadas(self):
        # Obtiene los recordatorios completados y los muestra en la interfaz de realizadas
        realizadas = [r for r in self.modelo.cargar_todos() if r.get('completado')]
        frame = self.vista.frames.get("RealizadasScreen")
        if frame and hasattr(frame, "realizadas_cont"):
            # Limpia el contenedor
            for widget in frame.realizadas_cont.winfo_children():
                widget.destroy()
            # Muestra cada recordatorio realizado
            from datetime import datetime
            hoy = datetime.today().date()
            for r in realizadas:
                fecha_completado = r.get('fecha_completado', '')
                # Determina si la tarea está atrasada
                atrasada = False
                if r.get('fecha'):
                    try:
                        fecha_tarea = datetime.strptime(r['fecha'], "%Y-%m-%d").date()
                        if fecha_tarea < hoy:
                            atrasada = True
                    except Exception:
                        pass
                # Icono: ticket si completado a tiempo, X si atrasada
                icono = "✔️" if not atrasada else "❌"
                texto = f"{icono} [{r.get('id')}] {r.get('titulo','')} - {r.get('hora','')} ({fecha_completado})"
                import tkinter as tk
                lbl = tk.Label(frame.realizadas_cont, text=texto, fg="#0f1722", bg="#ffffff", anchor="w")
                lbl.pack(fill="x", padx=8, pady=2)

    def crear_recordatorio(self, datos):
        self.modelo.guardar_recordatorio(datos)
        self.actualizar_pendientes_usuario()

    def eliminar_recordatorio(self, rec_id):
        self.modelo.eliminar_recordatorio(rec_id)
        self.actualizar_pendientes_usuario()

    def marcar_completado(self, rec_id):
        self.modelo.marcar_completado(rec_id)
        self.actualizar_pendientes_usuario()

    def obtener_recordatorios(self):
        return self.modelo.cargar_todos()

    def ejecutar(self):
        self.vista.mainloop()

    def on_crear_evento(self):
        from calendario import Calendario
        calendario = Calendario()
        calendario.seleccionar_fecha(self.vista.abrir_plantilla_agregar_evento)

    def crear_recordatorio_desde_vista(self):
        # Obtiene la pantalla de agregar recordatorio
        recordatorio_screen = self.vista.frames.get("RecordatorioScreen")
        if not recordatorio_screen:
            return
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

        # --- DEPURACIÓN: imprime los datos y tipos ---
        print("DEBUG datos:", {
            "titulo": titulo, "hora": hora, "repetir": repetir, "importante": importante,
            "dias": dias, "mantener": mantener, "alarma": alarma, "sonido": sonido, "fecha": fecha
        })
        print("DEBUG tipos:", {
            "titulo": type(titulo), "hora": type(hora), "repetir": type(repetir), "importante": type(importante),
            "dias": type(dias), "mantener": type(mantener), "alarma": type(alarma), "sonido": type(sonido), "fecha": type(fecha)
        })

        # --- Validación robusta ---
        if not titulo or not hora or not fecha or not isinstance(fecha, str) or len(fecha) < 8:
            from tkinter import messagebox
            messagebox.showerror("Error", "Debes completar título, hora y seleccionar una fecha válida.")
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
            "fecha": fecha
        }
        print("Intentando guardar recordatorio:", datos)
        self.crear_recordatorio(datos)
        # Vuelve a la pantalla anterior (usuario o admin)
        self.vista.cambiar_pantalla(self.vista.pantalla_anterior or "UsuarioScreen")


