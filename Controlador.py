from Modelo import MemoriaModelo
from Interfaz import App
import os

class Controlador:
    def __init__(self):
        # Asegura que el archivo recordatorios.json exista
        self._asegurar_archivo_json()
        self.modelo = MemoriaModelo()
        self.vista = App(controlador=self)
        # Puedes inicializar la vista con datos del modelo aquí si lo necesitas

    def _asegurar_archivo_json(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, 'recordatorios.json')
        if not os.path.exists(data_path):
            with open(data_path, 'w', encoding='utf-8') as f:
                f.write('[]')

    # Métodos para conectar eventos de la vista con el modelo
    def leer_pendientes(self):
        self.modelo.leer_pendientes()

    def crear_recordatorio(self, datos):
        self.modelo.guardar_recordatorio(datos)
        # Aquí podrías actualizar la vista si es necesario

    def eliminar_recordatorio(self, rec_id):
        self.modelo.eliminar_recordatorio(rec_id)
        # Actualizar la vista si es necesario

    def marcar_completado(self, rec_id):
        self.modelo.marcar_completado(rec_id)
        # Actualizar la vista si es necesario

    def obtener_recordatorios(self):
        return self.modelo.cargar_todos()

    # Agrega aquí más métodos según las necesidades de la interfaz

    def ejecutar(self):
        self.vista.mainloop()

# Si quieres ejecutar el controlador directamente:
if __name__ == "__main__":
    Controlador().ejecutar()
