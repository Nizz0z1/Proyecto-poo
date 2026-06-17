"""
Punto de entrada principal.
Lanza la interfaz gráfica (tkinter).
"""

from app.controllers.gestor_controller_gui import GestorControllerGUI


def main():
    app = GestorControllerGUI()
    app.ejecutar()


if __name__ == "__main__":
    main()
