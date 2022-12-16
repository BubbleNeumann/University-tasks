import sys

from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QWidget,
                             QLineEdit, QCheckBox, QPushButton)
import cx_Oracle

try:
    connection=cx_Oracle.connect('cdk_6309/1')
except cx_Oracle.DatabaseError:
    print ("Logon  Error:")
    exit(0)


class MainWindow(QWidget):
    """Main window is created at the application start."""

    def __init__(self):
        super().__init__()
        self.modif_window = None
        self.report_window = None
        self.check_participants = None
        self.check_papers = None
        self.setGeometry(500, 500, 500, 350)  # left, top, width, height
        self.setLayout(self.create_layout())

    @staticmethod
    def get_available_actions() -> list:
        return ['display table', 'add row', 'update row', 'delete row']

    def show_report_window(self) -> None:
        if self.report_window is None:
            self.report_window = ReportWindow('papers')

        self.report_window.show()

    def show_modif_window(self, action: str) -> None:
        
        
        if self.modif_window is None:
            self.modif_window = ModifWindow(action, 'papers')        
        
        for condition_field in self.modif_window.qlineedit_conditions:
            condition_field.setEnabled(action == 'upd' or action == 'del')
            
        for new_values_field in self.modif_window.qlineedit_new_values:
            new_values_field.setEnabled(action == 'upd' or action == 'add')
            
        self.modif_window.qlineedit_new_values[0].setEnabled(action != 'add')
        
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
            layout.addWidget(buttons[i], i+2, 0)

        return layout


class ModifWindow(QWidget):
    """Modification window requests field values from user."""

    def __init__(self, action, table):
        super().__init__()
        self.qlineedit_conditions = []
        self.qlineedit_new_values = []
        self.qlineedit_conditions_part = []
        self.qlineedit_new_values_part = []
        self.setLayout(self.create_layout(action, table))

    @staticmethod
    def get_papers_fields() -> list:
        return ['id_r', 'Title', 'id', 'Type', 'SectionName', 'SDate']
    
    @staticmethod
    def get_participants_fields() -> list:
        return ['id', 'Fname', 'AcademicDegree', 'PlaceOfWork', 'Position', 'Citizenship', 'BDate']

    @staticmethod
    def agregate_params(new_values: list, table: str) -> str:
        """Called for update and delete."""
        new_values_str = ''
        if table == 'papers':
            fields = ModifWindow.get_papers_fields()
        else:
            fields = ModifWindow.get_participants_fields()
            
        for i in range(0, len(new_values)):
            if new_values[i] != '':
                new_values_str = fields[i] + '='
                if table == 'papers':
                    if i == 1 or i == 3 or i == 5:
                        new_values_str += f'\'{new_values[i]}\''
                    else:
                        new_values_str += new_values[i]
                else:
                    if i == 0:
                        new_values_str += new_values[i]
                    else:
                        new_values_str += f'\'{new_values[i]}\''

        return new_values_str
    
    @staticmethod
    def convert_vals_to_str(vals: list, table: str) -> str:
        """Called for insert."""
        res = ''
        for i in range(1, len(vals)):
            if table == 'papers':
                if i == 1 or i == 3 or i == 5:
                    res += f'\'{vals[i]}\','
                else:
                    res += f'{vals[i]},'
            else:
                res += f'{vals[i]},'
                
        return res[:-1]

    @staticmethod
    def modify_table(action: str, conditions, new_values, table: str) -> None:
        request = ''
        cursor = connection.cursor()
        if action == 'upd':       
            vals = ModifWindow.agregate_params(new_values, table)
            where = ModifWindow.agregate_params(conditions, table)
            request = f'update {table} set {vals} where {where}'           
        elif action == 'add':
            if table == 'papers':
                cursor.execute('select max(id_r) from papers')
            else:
                cursor.execute('select max(id) from participants')
            next_id = cursor.fetchall()
            cursor.close()
            cursor = connection.cursor()
            vals = ModifWindow.convert_vals_to_str(new_values, table)
            request = f'insert into {table} values ({next_id[0][0]+1},{vals})'
        else:
            where = ModifWindow.agregate_params(conditions, table)
            request = f'delete from {table} where {where}'
            
        print(request)
        
        try:
            cursor.execute(request)
            connection.commit()
        except cx_Oracle.DatabaseError:
            print('cx_Oracle.DatabaseError')
        
        cursor.close()

    def on_submit(self, action: str, table: str) -> None:
        # TODO check if len(new_values) == 1
        conditions = []
        new_values = []
        counter = 0
        
        if table == 'papers':
            for i in range(0, len(self.qlineedit_conditions)):
                conditions.append(self.qlineedit_conditions[i].text())
                new_values.append(self.qlineedit_new_values[i].text())
                self.qlineedit_conditions[i].clear()
                self.qlineedit_new_values[i].clear()
                counter += int(new_values[i] != '')
        else:
            for i in range(0, len(self.qlineedit_conditions_part)):
                conditions.append(self.qlineedit_conditions_part[i].text())
                new_values.append(self.qlineedit_new_values_part[i].text())
                self.qlineedit_conditions_part[i].clear()
                self.qlineedit_new_values_part[i].clear()
                counter += int(new_values[i] != '')
            
        if action == 'add' and ((counter != 5 and table == 'papers') or (counter != 6 and table != 'papers')):
            pass
        else:
            ModifWindow.modify_table(action, conditions, new_values, table)
            self.close()

    def create_layout(self, action, table) -> QGridLayout:
        layout = QGridLayout()
        
        # papers layout
        lables = [QLabel(field + ' = ', self)
                  for field in ModifWindow.get_papers_fields()]
        
        self.qlineedit_conditions = [QLineEdit(self) for _ in lables]
        self.qlineedit_new_values = [QLineEdit(self) for _ in lables]
        
        
        for i in range(0, len(lables)):
            layout.addWidget(lables[i], i, 0)
            layout.addWidget(self.qlineedit_conditions[i], i, 1)
            layout.addWidget(self.qlineedit_new_values[i], i, 2)

        submit_btn = QPushButton('submit papers')
        submit_btn.clicked.connect(lambda: self.on_submit(action, table))
        layout.addWidget(submit_btn, len(lables), 2)
        
        # participants layout
        lables_p = [QLabel(field + ' = ', self)
                  for field in ModifWindow.get_participants_fields()]
        
        self.qlineedit_conditions_part = [QLineEdit(self) for _ in lables_p]
        self.qlineedit_new_values_part = [QLineEdit(self) for _ in lables_p]
        
        
        for i in range(0, len(lables_p)):
            layout.addWidget(lables_p[i], i+len(lables)+1, 0)
            layout.addWidget(self.qlineedit_conditions_part[i], i+len(lables)+1, 1)
            layout.addWidget(self.qlineedit_new_values_part[i], i+len(lables)+1, 2)

        submit_btn_part = QPushButton('submit participants')
        submit_btn_part.clicked.connect(lambda: self.on_submit(action, 'participants'))
        layout.addWidget(submit_btn_part, len(lables_p)+len(lables)+1, 2)
        
        
        return layout


class ReportWindow(QWidget):
    """Dump all data table contains as a table."""

    def __init__(self, table):
        super().__init__()
        self.setLayout(self.create_layout(table))
        self.show()
             
    def create_layout(self, table) -> QGridLayout:
        layout = QGridLayout()
        cursor = connection.cursor()       
        cursor.execute(f'select * from {table}')
        # cursor.execute('select * from papers')
        select_res = cursor.fetchall()
        layout.addWidget(QLabel(table))
        
        for tup in select_res:
            label_text = ''
            for elem in tup:
                label_text += elem.__str__() + ' | '
                
            layout.addWidget(QLabel(label_text))
            
        cursor.close()
        return layout


def main() -> None:    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
