import json
from models import Student, LabWorkSession

def load_students_json(file_path: str):
    """
    Загрузка списка студентов из json файла.
    Ошибка создания экземпляра класса Student не должна приводить к поломке всего чтения.
    """
    def parse_lab_work_session(json_list) -> list[LabWorkSession]:
        res = []
        for e in json_list:
            lab_works_ses = LabWorkSession(date=e['date'],presence=e['presence'],lab_n=e['lab_work_n'],mark=e['lab_work_mark'])
            res.append(lab_works_ses)

        return res

    with open(file_path) as f:
        res = []
        raw_json = json.load(f)
        for e in raw_json['students']:
            print(e)
            student = Student(
                    unique_id = e['unique_id'],
                    name = e['name'],
                    surname=e['surname'],
                    group=e['group'],
                    subgroup=e['subgroup'],
                    lab_work_sessions=parse_lab_work_session(e['lab_works_sessions'])
                    )
            res.append(student)
    return res

def save_students_json(file_path: str, students: list[Student]):
    res = '{"students":['
    for student in students:
        res += student.write_one_to_json() + ','
    res += ']}'
    with open(file_path, 'w') as out:
        out.write(res)

def main():
    students = load_students_json('students.json')
    
    save_students_json('students_saved.json', students)
    students = load_students_json('students_saved.json')
    
    # students = load_students_csv('students.csv')
    # students = save_students_csv('students_saved.csv')
    # load_students_csv('students_saved.csv', students)
    
    for s in students:
        print(s)

if __name__ == '__main__':
    main()
