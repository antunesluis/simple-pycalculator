import sys

from widgets.main_window import MainWindow
from variables import WINDOW_ICON_PATH
from widgets.display import Display
from widgets.info import Info
from widgets.styles import setupTheme

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication)


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Info
    info = Info('25.53 ^ 43.6 = 2345.43')
    window.addToVLayout(info)

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # display
    display = Display()
    window.addToVLayout(display)

    # Executa tudo
    window.AdjustFixedSize()
    window.show()
    app.exec()
