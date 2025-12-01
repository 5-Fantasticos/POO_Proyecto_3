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
        # Obtiene los recordatorios no completados y los muestra en la interfaz
        pendientes = [r for r in self.modelo.cargar_todos() if not r.get('completado')]
        frame = self.vista.frames.get("UsuarioScreen")
        if frame and hasattr(frame, "usuario_cont"):
            # Limpia el contenedor
            for widget in frame.usuario_cont.winfo_children():
                widget.destroy()
            # Muestra cada recordatorio pendiente
            for r in pendientes:
                texto = f"[{r.get('id')}] {r.get('titulo','')} - {r.get('hora','')}"
                import tkinter as tk
                # match Interfaz palette (card background with dark text)
                lbl = tk.Label(frame.usuario_cont, text=texto, fg="#0f1722", bg="#ffffff", anchor="w")
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


