import sqlite3

class Student:
    def __init__(self,name,surname,middle_name,group,grades):
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.group = group
        if len(grades) != 4:
            raise ValueError("Успеваемость должна содержать 4 оценки")
        self.grades = grades

def display_students():
    cursor.execute("SELECT * FROM Student")
    all_rows = cursor.fetchall()

    print()
    print("Все студенты:")
    for row in all_rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Отчество: {row[3]}, "
              f"Группа: {row[4]}, Средний балл: {row[5]}")
    print()

def input_student(return_as=False):
    print("Введите данные студента:")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    middle_name = input("Отчество: ")
    group = input("Группа: ")
    grade = input("Оценки (Вводить через пробел): ")
    student_information,grades = [],[]
    for i in range(len(grade)):
        if grade[i] == " ":
            pass
        else:
            grades.append(float(grade[i]))
    student_information.extend([name,surname,middle_name,group,grades])
    return student_information if return_as else Student(name, surname, middle_name, group, grades)

def add_student(student):
    average = sum(student.grades) / 4
    cursor.execute("""
        INSERT INTO Student 
        (name, surname, middle_name, groups, average_score)
        VALUES (?, ?, ?, ?, ?)
        """, (
            student.name,
            student.surname,
            student.middle_name,
            student.group,
            average
            ))
    connect.commit()

connect = sqlite3.connect("Student.db")
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Student
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                middle_name TEXT,
                groups INTEGER,
                average_score REAL)
                """)
connect.commit()

while True:
    print("1 - Добавить нового студента\n"
        "2 - Просмотр всех студентов\n"
        "3 - Просмотр одного студента\n"
        "4 - Редактирование студента\n"
        "5 - Удаление студента\n"
        "6 - Средний балл студентов группы\n"
        "7 - Завершить программу")

    action = int(input("Выберите действие: "))

    if action == 1:
        student = input_student()
        add_student(student)
        print("Cтудент успешно добавлен")

    elif action == 2:
        display_students()

    elif action == 3:
        id_student = input("Введите ID студента для вывода: ")
        cursor.execute("SELECT * FROM Student WHERE id = ?", (id_student,))
        row = cursor.fetchone()
        print(f"Имя: {row[1]}, Фамилия: {row[2]}, Отчество: {row[3]}, "
                f"Группа: {row[4]}, Средний балл: {row[5]}\n")

    elif action == 4:
        display_students()
        id_student = input("Выберите студента для редактирования: ")
        student_info = input_student(return_as=True)
        average = sum(student_info[4]) / 4
        cursor.execute("""
                    UPDATE Student SET 
                    name = ?, 
                    surname = ?, 
                    middle_name = ?, 
                    groups = ?, 
                    average_score = ? 
                    WHERE id = ?
                    """, (
            student_info[0],
            student_info[1],
            student_info[2],
            student_info[3],
            average,
            id_student
        ))
        connect.commit()
        print("Данные обновлены")
    elif action == 5:
        display_students()
        id_student = input("Выберите ID студента для удаления: ")
        cursor.execute("DELETE FROM Student WHERE id = ?", (id_student,))

        if cursor.rowcount > 0:
            print(f"Студент удалён!")
        else:
            print("Студент не найдена.")
        connect.commit()

    elif action == 6:
        display_students()
        summ = 0
        divider = 0
        group_number = input("Введите группу для вывода среднего балла: ")
        cursor.execute("SELECT * FROM Student WHERE groups = ?",(group_number,))
        for row in cursor:
            summ += float(row[5])
            divider += 1
        print(round(summ/divider,2))

    elif action == 7:
        break
