import sys

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QWidget,
                             QLineEdit, QVBoxLayout, QPushButton)


class MainWindow(QWidget):
    @staticmethod
    def get_available_actions() -> list:
        return ['display table', 'add row', 'update row', 'delete row']

    def show_report_window(self) -> None:
        pass

    def show_modif_window(self, action: str) -> None:
        if self.modif_window is None:
            self.modif_window = ModifWindow()

        self.modif_window.text_areas[0].setEnabled(action != 'add')
        self.modif_window.show()

    def create_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        buttons = [QPushButton(action)
                   for action in MainWindow.get_available_actions()]

        buttons[0].clicked.connect(self.show_report_window)
        buttons[1].clicked.connect(lambda: self.show_modif_window('add'))
        buttons[2].clicked.connect(lambda: self.show_modif_window('upd'))
        buttons[3].clicked.connect(lambda: self.show_modif_window('del'))

        for btn in buttons:
            layout.addWidget(btn)

        return layout

    def __init__(self):
        super().__init__()
        self.modif_window = None
        self.report_window = None
        self.setGeometry(1000, 1000, 500, 350)
        self.setLayout(self.create_layout())


class ModifWindow(QWidget):
    @staticmethod
    def get_available_fields() -> list:
        return ['id_r', 'Title', 'id', 'Type', 'SectionName', 'SDate']

    def on_submit(self) -> None:
        for text_area in self.text_areas:
            if text_area.text() != '':
                print(text_area.text())

        self.close()

    def create_layout(self) -> QGridLayout:
        layout = QGridLayout()
        lables = [QLabel(field + ' = ', self)
                  for field in ModifWindow.get_available_fields()]
        self.text_areas = [QLineEdit(self) for _ in lables]
        for i in range(0, len(lables)):
            layout.addWidget(lables[i], i, 0)
            layout.addWidget(self.text_areas[i], i, 1)

        submit_btn = QPushButton('submit')
        submit_btn.clicked.connect(self.on_submit)
        layout.addWidget(submit_btn, len(lables), 1)
        return layout

    def __init__(self):
        super().__init__()
        self.text_areas = []
        self.setLayout(self.create_layout())


class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()


def main() -> None:
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
