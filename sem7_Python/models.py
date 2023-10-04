class LabWorkSession:
    def __init__(self, date, presence: int, lab_n: int, mark:int):
        self.date = date
        self.presence = presence if presence == 0 or presence == 1 else None
        self.lab_n = lab_n if lab_n >= 0 else None
        self.mark = mark if 1 <=mark <=5 else None

    def write_one_to_json(self):
        return '{'+f'\n"presence":{self.presence},\n"lab_work_n":{self.lab_n},\n"lab_work_mark":{self.mark},\n"date":"{self.date}"'+'\n},\n'

    def __str__(self) -> str:
        return f'date={self.date},presence={self.presence},lab_n={self.lab_n},mark={self.mark}'


class Student:
    def __init__(self, unique_id: int, name: str, surname: str, group: int, subgroup: int, lab_work_sessions:list[LabWorkSession]):
        self.unique_id = unique_id
        self.name = name
        self.surname = surname
        self.group = None if group < 0 else group
        self.subgroup = None if subgroup < 0 else subgroup
        self.lab_work_sessions = lab_work_sessions
    
    def write_one_to_json(self):
        str_lab_work_sess = '['
        for e in self.lab_work_sessions:
            str_lab_work_sess += e.write_one_to_json()
        str_lab_work_sess = str_lab_work_sess[:-2]
        # print(str_lab_work_sess[:-1] + ']\n')
        return '{'+f'"unique_id":{self.unique_id},"name":"{self.name}","surname":"{self.surname}","group":{self.group},"subgroup":{self.subgroup},"lab_works_sessions":{str_lab_work_sess}'+']\n}\n'


    def __str__(self) -> str:
        str_lab_work_sessions = ''
        for e in self.lab_work_sessions:
            str_lab_work_sessions += '{' + e.__str__() + '}'
        return f'id={self.unique_id},name={self.name},surname={self.surname},group={self.group},subgroup={self.subgroup},labs={str_lab_work_sessions}'
