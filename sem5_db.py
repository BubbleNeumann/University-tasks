import sys

from dataclasses import dataclass

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QWidget,
                             QLineEdit, QVBoxLayout, QPushButton)

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
def set_id(obj: Paper, action_prompt: str) -> None:

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
    msg = QLabel(f'ID of an object to {action_prompt}:', parent=ask_id_window)
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
def prompt_field_values(opt: str) -> None:
    obj_names = ['id_r', 'Title', 'id', 'Type', 'SectionName', 'SDate']
    submit_button = QPushButton('submit')
    # layout.itemAtPosition()

    if (opt == 'add'):
        layout_elems = obj_names.copy()
        layout_elems.remove('id_r')
        add_row(layout_elems, submit_button)
    elif (opt == 'upd'):
        update_row(obj_names, submit_button)
    else:
        delete_row()


def on_submit(layout: QGridLayout, action: str):
    # TODO: read values from QLineEdit fields
    modif_window.close()
    # modif_window.layout().removeWidget()
    # modif_window.windowType


def add_row(layout_elems: list, submit_button: QPushButton):
    layout = QGridLayout()
    for i in range(0, len(layout_elems)):
        layout.addWidget(QLabel(layout_elems[i], parent=modif_window), i, 0)
        layout.addWidget(QLineEdit(modif_window), i, 1)

    submit_button.clicked.connect(lambda: on_submit(layout, action='add'))
    layout.addWidget(submit_button, len(layout_elems), 1)
    modif_window.setLayout(layout)
    modif_window.show()


def update_row(layout_elems: list, submit_button: QPushButton):
    layout = QGridLayout()
    for i in range(0, len(layout_elems)):
        layout.addWidget(QLabel(layout_elems[i], parent=modif_window), i, 0)
        layout.addWidget(QLineEdit(modif_window), i, 1)

    submit_button.clicked.connect(lambda: on_submit(layout, action='upd'))
    layout.addWidget(submit_button, len(layout_elems), 1)
    modif_window.setLayout(layout)
    modif_window.show()


def delete_row() -> None:
    paper = Paper()
    set_id(obj=paper, action_prompt='delete')


def show_main_window() -> None:
    layout = QVBoxLayout()
    main_window.setWindowTitle('opts')

    show_report_button = QPushButton('display info on papers')
    add_button = QPushButton('add row')
    update_button = QPushButton('update row')
    delete_button = QPushButton('delete row')

    show_report_button.clicked.connect(show_report_window)
    add_button.clicked.connect(lambda: prompt_field_values(opt='add'))
    delete_button.clicked.connect(delete_row)
    update_button.clicked.connect(lambda: prompt_field_values(opt='upd'))

    buttons = [value for name, value in locals().items()
               if name.endswith('_button')]

    for btn in buttons:
        layout.addWidget(btn)

    main_window.setGeometry(1000, 1000, 600, 500)  # left, top, width, height
    main_window.setLayout(layout)
    main_window.show()


def main() -> None:
    show_main_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
