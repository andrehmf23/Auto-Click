import keyboard
import pyautogui
from PyQt5 import QtCore, QtWidgets, QtGui

from view.component.hotbar import CustomHotBar
from view.component.square import CustomCheckBox

"""
container - widget
layout - layout

hotbar - widget

body - widget
layout body - layout
"""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoClicker")
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(350, 150)

        # Layout principal da janela
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setSpacing(0)

        # Widget principal
        widget_main = QtWidgets.QWidget()
        widget_main.setLayout(layout_main)

        # Widget principal da janela
        self.setCentralWidget(widget_main)

        """_____________________________________[HOTBAR]_____________________________________"""

        # Remove a barra de título e bordas da janela
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.hotbar = CustomHotBar(self)  # Instancia a barra de título
        layout_main.addWidget(self.hotbar)  # Adiciona ao layout principal

        """_____________________________________[LAYOUTS E WIDGETS]_____________________________________"""

        layout_body = QtWidgets.QVBoxLayout(widget_main)

        widget_body = QtWidgets.QWidget()
        layout_main.addWidget(widget_body)
        widget_body.setLayout(layout_body)
        widget_body.setStyleSheet("""
            background-color: #303841;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)

        """_____________________________________[LAYOUT TOOLS]_____________________________________"""

        tools_layout = QtWidgets.QHBoxLayout()

        # CheckBox
        self.checkbox = CustomCheckBox()
        tools_layout.addWidget(self.checkbox, alignment=QtCore.Qt.AlignLeft)

        # QLabel "timer"
        self.label_auto = QtWidgets.QLabel("Timer:", self)
        self.label_auto.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #EEEEEE;
            }
            """
        )
        tools_layout.addWidget(self.label_auto, alignment=QtCore.Qt.AlignLeft)

        # Input que aceita apenas números
        self.number_input = QtWidgets.QLineEdit()
        self.number_input.setPlaceholderText("...")
        self.number_input.setFixedSize(75, 30)
        self.number_input.setText('1')  # Valor padrão
        self.number_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #EEEEEE;
                font-size: 15px;
                border: 3px solid #3A4750;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 3px solid #F6C90E;
            }
            """
        )
        # Defina um validador para números de ponto flutuante
        validator = QtGui.QDoubleValidator(0.000, 999.999, 3)  # Aceita de 0.0 a 999.0 com até 2 casas decimais
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)  # Notação padrão
        validator.setLocale(QtCore.QLocale("en_US"))  # Garante que o ponto seja aceito como separador decimal
        self.number_input.setValidator(validator)

        self.number_input.textChanged.connect(self.on_text_changed)
        tools_layout.addWidget(self.number_input, alignment=QtCore.Qt.AlignLeft)

        # QLabel "auto"
        self.label_auto = QtWidgets.QLabel("Auto: ", self)
        self.label_auto.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #EEEEEE;
            }
            """
        )
        tools_layout.addWidget(self.label_auto, alignment=QtCore.Qt.AlignLeft)

        # QLabel "key"
        self.label_auto = QtWidgets.QLabel("Q", self)
        self.label_auto.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #EEEEEE;
            }
            """
        )
        tools_layout.addWidget(self.label_auto, alignment=QtCore.Qt.AlignLeft)

        # QLabel "timer"
        self.settings_button = QtWidgets.QPushButton("", self)
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                background-image: url('assets/settingsw.png');
                background-position: center;
                background-repeat: no-repeat;
            }
            QPushButton:hover {
                background-image: url('assets/settingsb.png');
            }
            QPushButton:pressed {
                background-image: url('assets/settingsy.png');
            }
            """
        )
        tools_layout.addWidget(self.settings_button, alignment=QtCore.Qt.AlignLeft)

        tools_widget = QtWidgets.QWidget()
        tools_widget.setLayout(tools_layout)

        layout_body.addWidget(tools_widget)

        """_____________________________________[END LAYOUT TOOLS]_____________________________________"""

        # QLabel para mostrar o progresso do temporizador
        self.timer_label = QtWidgets.QLabel("[ tap: 0 / 1.0 sec ]", self)
        self.timer_label.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
                color: #EEEEEE;
            }
            """
        )
        layout_body.addWidget(self.timer_label, alignment=QtCore.Qt.AlignCenter)

        # Variáveis de controle
        self.time_elapsed = 0
        self.timer_average = float(self.number_input.text())  # Inicializa com o valor do input

        # Criação e configuração do temporizador
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(int(1000 * self.timer_average))  # Reinicia o temporizador

        # Inicia a captura global
        self.start_key_listener()

    """
    def keyPressEvent(self, event):
        Captura eventos de tecla pressionada.
        if event.key() == self.expected_key:
            self.checkbox.setChecked(not self.checkbox.isChecked())
        else:
            self.timer_label.setText("Tecla incorreta. Tente novamente!")
    """

    def start_key_listener(self):
        """Inicia o monitoramento de teclas globalmente."""
        keyboard.add_hotkey('q', self.on_key_press, args=('Q',))

    def on_key_press(self, key):
        """Ação executada quando a tecla 'Q' for pressionada."""
        self.checkbox.setChecked(not self.checkbox.isChecked())
        print(f"A tecla '{key}' foi pressionada!")  # Também loga no terminal

    def closeEvent(self, event):
        """Remove os ganchos globais ao fechar a aplicação."""
        keyboard.unhook_all_hotkeys()
        super().closeEvent(event)

    def update_timer(self):
        """Atualiza o progresso do temporizador e verifica o limite."""
        self.time_elapsed += 1
        if self.checkbox.isChecked():
            pyautogui.click()
        self.timer_label.setText(f"[ tap: {self.time_elapsed} / {self.timer_average} sec ]")

    def on_text_changed(self):
        """Atualiza o limite do temporizador quando o texto mudar."""
        text = self.number_input.text()
        if text and self.number_input.hasAcceptableInput():
            self.timer_average = float(text)  # Atualiza o limite
            self.timer_label.setText(f"[ tap: {self.time_elapsed} / {self.timer_average} sec ]")
            self.timer.start(int(1000 * self.timer_average))  # Reinicia o temporizador
