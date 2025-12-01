"""Main solo para mostrar la pantalla del usuario usando Tkinter."""

from Controlador import Controlador

def main():
    # Usar el controlador para que la interfaz se conecte al modelo y lea el .json
    controlador = Controlador()
    controlador.vista.cambiar_pantalla("UsuarioScreen")
    controlador.ejecutar()

if __name__ == "__main__":
    main()

