import sys

from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QWidget,
                             QLineEdit, QCheckBox, QPushButton)

# globals
bg = '#a32a8d'
fg = '#ebd8e7'

class MainWindow(QWidget):
    """Main window is created at the application start."""

    def __init__(self):
        super().__init__()
        self.modif_window = None
        self.report_window = None
        self.setGeometry(1000, 1000, 500, 210)  # left, top, width, height
        self.setLayout(self.create_layout())

    @staticmethod
    def get_available_actions() -> list:
        return ['report', 'add row', 'update table', 'delete row']

    def show_report_window(self) -> None:
        if self.report_window is None:
            self.report_window = ReportWindow()

        self.report_window.show()

    def show_modif_window(self, action: str) -> None:
        if self.modif_window is None:
            self.modif_window = ModifWindow()

        self.modif_window.text_areas[0].setEnabled(action != 'add')
        for checkbox in self.modif_window.checkboxes:
            checkbox.setEnabled(action == 'upd')
            
        self.modif_window.show()

    def create_layout(self) -> QGridLayout:
        layout = QGridLayout()
        buttons = [QPushButton(action)
                   for action in MainWindow.get_available_actions()]

        buttons[0].clicked.connect(self.show_report_window)
        buttons[1].clicked.connect(lambda: self.show_modif_window('add'))
        buttons[2].clicked.connect(lambda: self.show_modif_window('upd'))
        buttons[3].clicked.connect(lambda: self.show_modif_window('del'))

        for i in range(0, len(buttons)):
            buttons[i].setStyleSheet(f'background-color:{bg}; color:{fg}')
            buttons[i].setFixedWidth(230)
            layout.addWidget(buttons[i], i%2, i//2)

        return layout


class ModifWindow(QWidget):
    """
    Modification window requests field values from user.
    Checked checkbox => field value is an update condition.
    """

    def __init__(self):
        super().__init__()
        self.checkboxes = []
        self.text_areas = []
        self.setLayout(self.create_layout())

    @staticmethod
    def get_available_fields() -> list:
        return ['id_r', 'Title', 'id', 'Type', 'SectionName', 'SDate']

    def on_submit(self) -> None:
        # if needed create new class properties:
        field_values = []
        checkboxes_values = []

        # example how to get widgets' values
        # assemble update request based on this
        for i in range(len(self.text_areas)):
            field_values.append(self.text_areas[i].text())
            checkboxes_values.append(self.checkboxes[i].isChecked())
            self.text_areas[i].clear()
            self.checkboxes[i].setChecked(False)

        print(checkboxes_values)
        self.close()

    def create_layout(self) -> QGridLayout:
        layout = QGridLayout()
        lables = [QLabel(field + ' = ', self)
                  for field in ModifWindow.get_available_fields()]
        
        self.text_areas = [QLineEdit(self)  for _ in lables]
        self.checkboxes = [QCheckBox(self) for _ in lables]

        layout.addWidget(QLabel('* check = update condition'), 0, 2)
        for i in range(0, len(lables)):
            layout.addWidget(self.checkboxes[i], i+1, 0)
            layout.addWidget(lables[i], i+1, 1)
            layout.addWidget(self.text_areas[i], i+1, 2)

        submit_btn = QPushButton('submit')
        submit_btn.setStyleSheet(f'background-color:{bg}; color:{fg}')
        submit_btn.clicked.connect(self.on_submit)
        layout.addWidget(submit_btn, len(lables)+1, 2)
        return layout


class ReportWindow(QWidget):
    """Dump all data db contains as a table."""

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

