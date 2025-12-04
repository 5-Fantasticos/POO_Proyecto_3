# MediReminder

Aplicación de recordatorios de medicación desarrollada en Python con Tkinter.

## Características

- Crear, editar y eliminar recordatorios de medicamentos.
- Visualización de tareas pendientes solo para el día actual.
- Historial de tareas completadas y eliminadas.
- Interfaz inspirada en Medisafe.
- Selección de fecha mediante calendario.
- Soporte para repetición diaria, semanal y mensual.
- Distintivo visual para tareas eliminadas y completadas.

## Estructura del proyecto

- `main.py`: Punto de entrada de la aplicación.
- `Controlador.py`: Lógica de conexión entre la interfaz y el modelo.
- `Interfaz.py`: Interfaz gráfica de usuario (Tkinter).
- `Modelo.py`: Gestión de datos y lógica de recordatorios.
- `calendario.py`: Componente de calendario para selección de fechas.
- `recordatorios.json`: Archivo donde se almacenan los recordatorios.

## Requisitos

- Python 3.8 o superior.
- Paquete `Pillow` para imágenes en el calendario (`pip install pillow`).

## Uso

- Desde la pantalla principal puedes acceder a tus recordatorios, crear nuevos, editar o eliminar.
- Para eliminar un recordatorio, haz clic derecho sobre él en la lista de eventos.
- Para editar, haz doble clic sobre el evento.
- Las tareas eliminadas aparecen en el historial con un distintivo ❌.
- Las tareas completadas aparecen con un distintivo ✔️.

## Autor

Equipo de desarrollo POO Proyecto 3|| 5-Fantasticos.
