"""Main unificado para usuario y pariente (administrador) usando Tkinter."""

import tkinter as tk
from Interfaz import App  # Usa la clase App de la migración Tkinter

def main():
    root_app = App()
    root_app.cambiar_pantalla("UsuarioScreen")
    root_app.mainloop()

if __name__ == "__main__":
    main()

