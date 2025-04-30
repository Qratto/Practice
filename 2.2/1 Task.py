class Student:
    def __init__(self,surname,date_birth,group,grades):
        self.surname = surname
        self.date_birth = date_birth
        self.group = group
        if len(grades) != 5:
            raise ValueError("Успеваемость должна содержать ровно 5 оценок")
        self.grades = grades

    def print_information(self):
        print(f"Фамилия {self.surname}, группа {self.group}, дата прождения {self.date_birth}")
        print(f"Успеваемость: {', '.join(map(str, self.grades))}")

    def set_surname(self,new_surname):
        self.surname = new_surname

    def set_birth_date(self, date_birth):
        self.date_birth = date_birth

    def set_group_number(self, new_group):
        self.group = new_group
Tom = Student("Шкарупин", "20.07.2007",632,[5,2,5,2,5])
Tom.print_information()
Tom.set_surname("Сабельфельд")
Tom.print_information()

