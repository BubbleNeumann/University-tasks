from collections.abc import Generator
import sys
import json
from models import Student, LabWorkSession

def load_students_json(file_path: str) -> Generator[Student, None, None]:
    def parse_lab_work_session(json_list) -> Generator[LabWorkSession, None, None]:
        yield from list(LabWorkSession(date=e['date'],presence=e['presence'],lab_n=e['lab_work_n'],mark=e['lab_work_mark']) for e in json_list)

    with open(file_path) as f:
        for e in json.load(f)['students']:
            try:
                yield Student(
                    unique_id = e['unique_id'],
                    name = e['name'],
                    surname=e['surname'],
                    group=e['group'],
                    subgroup=e['subgroup'],
                    lab_work_sessions=list(parse_lab_work_session(e['lab_works_sessions']))
                    )
            except e:
                continue

def save_students_json(file_path: str, students: list[Student]):
    res = '{"students":[\n'
    for student in students:
        res += student.write_one_to_json() + ','
    with open(file_path, 'w') as out:
        out.write(res[:-1] + ']}')


def load_students_csv(file_path: str) -> Generator[Student, None, None]:
    def parse_lab_work_session(csv_list: list[str]) -> LabWorkSession:
        return LabWorkSession(
                date=csv_list[0],
                presence=int(csv_list[1]),
                lab_n=int(csv_list[2]),
                mark=int(csv_list[3])
                )

    with open(file_path) as f:
        for line in f.readlines()[1:]:
            line_list = line.split(';')
            student = Student(
                    unique_id=int(line_list[0]),
                    name=line_list[1],
                    surname=line_list[2],
                    group=int(line_list[3]),
                    subgroup=int(line_list[4]),
                    lab_work_sessions=[parse_lab_work_session(line_list[5:])]
                    )
            yield student

def save_students_csv(file_path: str, students: list[Student]):
    file_cont = 'unique_id;name;surname;group;subgroup;date;presence;lab_work_number;lab_work_mark\n'
    for s in students:
        file_cont += ';'.join([ str(e) for e in list(s.__dict__.values())[:-1]]) + ';' + ';'.join([str(e) for e in s.lab_work_sessions[0].__dict__.values()]) + '\n'
    with open(file_path, 'w') as f:
        f.write(file_cont)


def main(argv):
    if argv[0] == 'json':
        students = load_students_json('resources/students.json')
        save_students_json('resources/students_saved.json', list(students))
        students = load_students_json('resources/students_saved.json')
    elif argv[0] == 'csv':
        students = load_students_csv('resources/students.csv')
        save_students_csv('resources/students_saved.csv', list(students))
        students = load_students_csv('resources/students_saved.csv')
    else:
        print(f'unknown option {argv[0]}')
        return
    
    for s in students:
        print(s)


if __name__ == '__main__':
    main(sys.argv[1:])
