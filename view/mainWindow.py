import keyboard
import pyautogui
from PyQt5 import QtCore, QtWidgets, QtGui

from view.component.hotbar import CustomHotBar
from view.component.square import CustomCheckBox
from view.settingWindow import SettingWindow

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
        self.setFixedSize(450, 150)

        self.hold = False
        self.active_key = "q"
        self.setting_window = None

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
        self.label_key = QtWidgets.QLabel("Timer:", self)
        self.label_key.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #EEEEEE;
            }
            """
        )
        tools_layout.addWidget(self.label_key, alignment=QtCore.Qt.AlignLeft)

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
        self.label_key = QtWidgets.QLabel("Key: ", self)
        self.label_key.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #EEEEEE;
            }
            """
        )
        tools_layout.addWidget(self.label_key, alignment=QtCore.Qt.AlignRight)

        # QLabel "key"
        self.label_key = QtWidgets.QLabel("q", self)
        self.label_key.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #EEEEEE;
            }
            """
        )
        tools_layout.addWidget(self.label_key, alignment=QtCore.Qt.AlignLeft)

        # QLabel "timer"
        self.setting_button = QtWidgets.QPushButton("", self)
        self.setting_button.setFixedSize(40, 40)
        self.setting_button.setStyleSheet(
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
        self.setting_button.clicked.connect(self.open_setting_window)
        tools_layout.addWidget(self.setting_button, alignment=QtCore.Qt.AlignLeft)

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

    def start_key_listener(self):
        """Inicia o monitoramento de teclas globalmente."""
        keyboard.on_press_key(self.active_key, self.on_key_press)
        keyboard.on_release_key(self.active_key, self.on_key_release)

    def on_key_press(self, event):
        """Ação executada quando a tecla 'Q' for pressionada."""
        if (not self.hold) or (self.hold and not self.checkbox.isChecked()):
            self.checkbox.setChecked(not self.checkbox.isChecked())
            self.timer.start(int(1000 * self.timer_average))  # Reinicia o temporizador
            print("Auto-clique ativado!")

    def on_key_release(self, event):
        """Ação executada quando a tecla 'Q' for liberada."""
        if self.checkbox.isChecked() and self.hold:
            self.checkbox.setChecked(False)
            self.timer.stop()  # Para o temporizador
            print("Auto-clique desativado!")

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

    def open_setting_window(self):
        """Abre a janela de configuração sem fechar a janela principal."""
        if self.setting_window is None or not self.setting_window.isVisible():
            self.setting_window = SettingWindow(hold_ref=[self.hold], current_key=self.active_key)  # Passa referência de hold
            self.setting_window.hold_changed.connect(self.update_hold)  # Conecta sinal para sincronizar alterações
            self.setting_window.key_changed.connect(self.update_key)  # Conecta sinal
            self.setting_window.show()
        else:
            self.setting_window.raise_()
            self.setting_window.activateWindow()

    def update_key(self, new_key):
        """Atualiza a tecla usada para o auto-clique."""
        self.active_key = new_key
        self.label_key.setText(new_key)
        self.start_key_listener()  # Reinicia o listener com a nova tecla
        print(f"Tecla atualizada para: {self.active_key}")

    def update_hold(self, new_hold):
        """Atualiza o estado de hold baseado na configuração da SettingWindow."""
        self.hold = new_hold
        print(f"Novo estado de hold: {self.hold}")
