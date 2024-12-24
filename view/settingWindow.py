import keyboard
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtCore import pyqtSignal


class SettingWindow(QtWidgets.QWidget):
    hold_changed = pyqtSignal(bool)  # For hold changes
    key_changed = pyqtSignal(str)  # For key changes

    def __init__(self, hold_ref, current_key):
        super().__init__()
        self.hold_ref = hold_ref
        self.current_key = current_key

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)

        # Mostra o valor atual de hold
        self.label = QtWidgets.QLabel(f"Hold: {self.hold_ref[0]}")

        # Botão para alternar o valor de hold
        self.toggle_button = QtWidgets.QPushButton("Toggle Hold")
        self.toggle_button.clicked.connect(self.toggle_hold)

        # Label para mostrar a tecla ativa
        self.key_label = QtWidgets.QLabel(f"Tecla atual: {self.current_key}", self)
        self.key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_label.setStyleSheet("font-size: 16px; color: #EEEEEE;")

        # Botão para capturar a tecla
        self.capture_button = QtWidgets.QPushButton("Capturar Tecla", self)
        self.capture_button.clicked.connect(self.capture_key)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.key_label)
        layout.addWidget(self.capture_button)

        self.setLayout(layout)

    def capture_key(self):
        """Função para capturar a tecla pressionada."""
        self.setWindowTitle("Pressione a tecla desejada...")
        keyboard.hook(self.on_key_pressed)

    def on_key_pressed(self, event):
        """Atualiza a tecla quando uma tecla é pressionada."""
        self.current_key = event.name
        self.key_label.setText(f"Tecla atual: {self.current_key}")
        self.key_changed.emit(self.current_key)
        self.setWindowTitle("Configurações")  # Retorna ao título original
        keyboard.unhook_all()  # Remove o hook

    def toggle_hold(self):
        """Altera o valor de hold e emite um sinal com o novo estado."""
        self.hold_ref[0] = not self.hold_ref[0]
        self.label.setText(f"Hold: {self.hold_ref[0]}")
        self.hold_changed.emit(self.hold_ref[0])  # Emite o sinal
