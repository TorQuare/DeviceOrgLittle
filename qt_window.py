import sys
from PySide6.QtWidgets import *


class MainWindow(QWidget):

    __radiobutton_style = """
    QRadioButton::indicator {
                width: 0px;
                height: 0px;
            }
    QRadio
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setGeometry(100, 100, 400, 400)
        self.main_layout = QVBoxLayout()

    def render_window(self):
        self.main_layout.addLayout(self.__create_radiobutton())
        self.setLayout(self.main_layout)
        self.show()

    def __create_radiobutton(self):
        layout = QHBoxLayout()

        item_radio = QRadioButton("Lista przedmiotów")
        item_radio.setChecked(True)
        item_radio.setStyleSheet(self.__radiobutton_style)
        task_radio = QRadioButton("Lista zleceń")
        task_radio.setStyleSheet(self.__radiobutton_style)

        layout.addWidget(item_radio)
        layout.addWidget(task_radio)

        return layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.render_window()
    sys.exit(app.exec())
