from datetime import datetime

class Evento:
    def __init__(self, titulo, hora, dias, creador, estado="pendiente", nombre_alarma="JHON CENA SATURED"):
        self.titulo = titulo
        self.hora = hora
        self.dias = dias  
        self.creador = creador
        self.estado = estado
        self.nombre_alarma = nombre_alarma

    def __str__(self):
        dias_str = ",".join(self.dias)
        return f"{self.titulo}|{self.hora}|{dias_str}|{self.creador}|{self.estado}|{self.nombre_alarma}"

    def guardar(self):
        with open("eventos.txt", "a") as f:
            f.write(str(self) + "\n")
        Evento.registrar_historial(self.titulo, self.creador, "creó evento")

    @staticmethod
    def registrar_historial(evento_id, usuario, accion):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("historial.txt", "a") as f:
            f.write(f"{evento_id}|{usuario}|{accion}|{timestamp}\n")

    @staticmethod
    def leer_eventos():
        eventos = []
        try:
            with open("eventos.txt", "r") as f:
                for line in f:
                    partes = line.strip().split("|")
                    if len(partes) >= 6:
                        titulo, hora, dias, creador, estado, nombre_alarma = partes
                        eventos.append(Evento(titulo, hora, dias.split(","), creador, estado, nombre_alarma))
        except FileNotFoundError:
            pass
        return eventos


