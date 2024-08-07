import math
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton

from utils import isEmpty, isNumOrDot, isValidNumber, convertToNumber
from variables import MEDIUM_FONT_SIZE

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(76, 75)


class ButtonsGrid(QGridLayout):
    def __init__(
        self, display: "Display", info: "Info", window: "MainWindow", *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "D", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]
        self.info = info
        self.display = display
        self._equation = ""
        self.window = window
        self._equationInitValue = "Sua conta"
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, columnNumber)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == "C":
            self._connectButtonClicked(button, self._clear)

        if text == "D":
            self._connectButtonClicked(button, self.display.backspace)

        if text == "=":
            self._connectButtonClicked(button, self._eq)

        if text == "N":
            self._connectButtonClicked(button, self._invertNumber)

        if text in "+-/*^":
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, text))

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = convertToNumber(displayText)
        self.display.setText(str(number))

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)

        return realSlot

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()  # Devera ser meu número _left
        self.display.clear()  # Limpa o display
        self.display.setFocus()

        # Operador clicado sem nenhum número configurado.
        if not isValidNumber(displayText) and self._left is None:
            self._showError("Você não digitou nada.")
            return

        # Se ouver apenas o número da esquerda aguardamos o número da direita.
        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f"{self._left} {self._op} ??"

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError("Você não digitou o restante da conta")
            return

        self._right = convertToNumber(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"

        try:
            if "^" in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError("Divisão inválida.")
        except OverflowError:
            self._showError("Numero resultante muito grande.")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == "error":
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()

