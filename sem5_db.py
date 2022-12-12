import sys

from dataclasses import dataclass

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QWidget,
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

NO_ID = -1


@dataclass
class Paper:
    id_r: int = NO_ID
    id: int = NO_ID

    # needed when creating a new obj
    def assign_id(self):
        # get max id for id_r and id. assign corresponding fields with max+1
        pass


# set id field of Paper obj
def set_id(obj: Paper, action: str) -> None:

    # TODO: implement id check
    def id_is_valid(id: int) -> bool:
        return True

    def on_submit(text_area, ask_id_window) -> None:
        user_input = text_area.text()
        text_area.clear()
        if id_is_valid(int(user_input)):
            obj.id = user_input

        # TODO: reprompt user if id is not valid

        ask_id_window.close()

    ask_id_window.setGeometry(1000, 1000, 400, 200)
    layout = QVBoxLayout()
    msg = QLabel(f'ID of an object to {action}:', parent=ask_id_window)
    text_area = QLineEdit(parent=ask_id_window)
    text_area.setValidator(QIntValidator())
    submit_button = QPushButton('submit')
    submit_button.clicked.connect(lambda: on_submit(text_area, ask_id_window))
    layout.addWidget(msg)
    layout.addWidget(text_area)
    layout.addWidget(submit_button)
    ask_id_window.setLayout(layout)
    ask_id_window.show()


# display all data from papers as table
def show_report_window() -> None:
    report_window.setGeometry(2000, 1000, 600, 500)
    report_window.show()


# request data from user
# user shouldn't be able to edit id_r and id fields
def show_modif_window(update=False) -> None:

    def on_submit(modif_window):
        modif_window.close()

    paper = Paper()

    # layout = QVBoxLayout()
    layout = QGridLayout()
    submit_button = QPushButton('submit')

    if update:
        set_id(obj=paper, action='update')

    else:
        # get max id from db
        # id = max id + 1

        pass

    submit_button.clicked.connect(lambda: on_submit(modif_window))
    layout.addWidget(submit_button)
    modif_window.setLayout(layout)
    modif_window.show()


def delete_row() -> None:
    id = set_id(action='delete')


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
