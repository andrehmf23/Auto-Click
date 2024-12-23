from PyQt5 import QtWidgets, QtCore


class CustomHotBar(QtWidgets.QWidget):
    def __init__(self, parent_window: QtWidgets.QMainWindow):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.old_pos = None  # Armazena a posição anterior do mouse

        # Configuração visual da barra de título
        self.setStyleSheet("""
            background-color: #3A4750;  /* Cor de fundo */
        """)
        self.setFixedHeight(30)

        # Layout principal
        title_layout = QtWidgets.QHBoxLayout(self)
        title_layout.setContentsMargins(0, 0, 0, 0)  # Remove margens internas
        title_layout.setSpacing(0)

        # Espaço vazio à esquerda
        left_space = QtWidgets.QWidget()
        left_space.setStyleSheet("background-color: #3A4750;")  # Cor de fundo explícita para evitar transparência
        title_layout.addWidget(left_space, stretch=1)  # Espaço flexível

        # Botões de minimizar e fechar
        minimize_button = QtWidgets.QPushButton("_", self)
        minimize_button.setStyleSheet("""
            QPushButton {
                background: #3A4750;
                color: black;
                border: none;
            }
            QPushButton:hover {
                background: #EEEEEE;
                color: black;
            }
            QPushButton:pressed {
                background: #F6C90E;
                color: white;
            }
        """)
        minimize_button.setFixedSize(30, 30)
        minimize_button.clicked.connect(parent_window.showMinimized)

        close_button = QtWidgets.QPushButton("X", self)
        close_button.setStyleSheet("""
            QPushButton {
                background: #3A4750;
                color: black;
                border: none;
            }
            QPushButton:hover {
                background: red;
                color: white;
            }
            QPushButton:pressed {
                background: darkred;
            }
        """)
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(parent_window.close)

        # Adiciona os botões ao layout
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(close_button)

    def mousePressEvent(self, event):
        """Inicia o movimento da janela ao clicar na barra de título."""
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Move a janela enquanto arrasta."""
        if event.buttons() == QtCore.Qt.LeftButton and self.old_pos:
            self.parent_window.move(event.globalPos() - self.old_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Finaliza o movimento da janela."""
        self.old_pos = None
