from PyQt5 import QtWidgets


class CustomCheckBox(QtWidgets.QCheckBox):
    def __init__(self):
        super().__init__()
        self.setText("")  # Remove o texto padrão
        self.setFixedSize(40, 40)  # Tamanho fixo para o quadrado
        self.setStyleSheet(self.get_style())

        # Conecta o evento de estado alterado
        self.stateChanged.connect(self.update_style)

    def update_style(self):
        """Atualiza o estilo baseado no estado."""
        self.setStyleSheet(self.get_style())

    def get_style(self):
        """Retorna o estilo baseado no estado."""
        if self.isChecked():
            background_color = "#F6C90E"
            border_color = "#303841"
        else:
            background_color = "gray"
            border_color = "#303841"

        return f"""
            QCheckBox {{
                spacing: 0px;
            }}
            QCheckBox::indicator {{
                width: 30px;
                height: 30px;
                background-color: {background_color};
                border: 3px solid {border_color};
            }}
            QCheckBox::indicator:hover {{
                border: 3px solid #3A4750;
            }}
        """

