import sys

from variables import WINDOW_ICON_PATH

from widgets.main_window import MainWindow
from widgets.display import Display
from widgets.info import Info
from widgets.styles import setupTheme
from widgets.buttons import ButtonsGrid

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication)


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info)
    window.vLayout.addLayout(buttonsGrid)

    # Executa tudo
    window.AdjustFixedSize()
    window.show()
    app.exec()
