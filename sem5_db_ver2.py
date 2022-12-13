import sys

from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QWidget,
                             QLineEdit, QVBoxLayout, QPushButton)


class MainWindow(QWidget):
    """Main window is created at the application start."""

    def __init__(self):
        super().__init__()
        self.modif_window = None
        self.report_window = None
        self.setGeometry(1000, 1000, 500, 350)  # left, top, width, height
        self.setLayout(self.create_layout())

    @staticmethod
    def get_available_actions() -> list:
        return ['display table', 'add row', 'update row', 'delete row']

    def show_report_window(self) -> None:
        if self.report_window is None:
            self.report_window = ReportWindow()

        self.report_window.show()

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


class ModifWindow(QWidget):
    """Modification window requests field values from user."""

    def __init__(self):
        super().__init__()
        self.text_areas = []
        self.setLayout(self.create_layout())

    @staticmethod
    def get_available_fields() -> list:
        return ['id_r', 'Title', 'id', 'Type', 'SectionName', 'SDate']

    def on_submit(self) -> None:
        field_values = []
        for text_area in self.text_areas:
            field_values.append(text_area.text())
            text_area.clear()

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


class ReportWindow(QWidget):
    """Dump all data table contains as a table."""

    def __init__(self):
        super().__init__()

    def create_layout(self):
        pass


def main() -> None:
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
