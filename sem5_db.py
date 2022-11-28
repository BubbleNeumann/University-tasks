import sys

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget,
                             QLineEdit, QVBoxLayout, QPushButton, QMessageBox)

# globals
app = QApplication(sys.argv)
main_window = QWidget()
report_window = QWidget()
modif_window = QWidget()
ask_id_window = QWidget()

'''
TODO:
- connect to db
- assemble report window
- handle input from ask_id func
- create window for data modification
'''


def handle_inp():
    pass


def ask_id(action: str):
    ask_id_window.setGeometry(1000, 1000, 400, 200)
    layout = QVBoxLayout()
    msg = QLabel(f'ID of an object to {action}:', parent=ask_id_window)
    text_area = QLineEdit(parent=ask_id_window)
    text_area.setValidator(QIntValidator())
    submit_button = QPushButton('submit')
    submit_button.clicked.connect(handle_inp)
    layout.addWidget(msg)
    layout.addWidget(text_area)
    layout.addWidget(submit_button)
    ask_id_window.setLayout(layout)
    ask_id_window.show()


def show_report_window() -> None:
    report_window.setGeometry(2000, 1000, 600, 500)
    report_window.show()


def show_modif_window(update=False) -> None:
    if update:
        id = ask_id('update')

    modif_window.show()


def delete_row() -> None:
    id = ask_id(action='delete')


def main() -> None:
    layout = QVBoxLayout()
    main_window.setWindowTitle('opts')

    show_report_button = QPushButton('display info on papers')
    add_button = QPushButton('add row')
    delete_button = QPushButton('delete row')
    update_button = QPushButton('update row')

    show_report_button.clicked.connect(show_report_window)
    add_button.clicked.connect(show_modif_window)
    delete_button.clicked.connect(delete_row)
    update_button.clicked.connect(lambda: show_modif_window(update=True))

    buttons = [value for name, value in locals().items()
               if name.endswith('_button')]

    for btn in buttons:
        layout.addWidget(btn)

    main_window.setGeometry(1000, 1000, 600, 500)  # left, top, width, height
    main_window.setLayout(layout)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
