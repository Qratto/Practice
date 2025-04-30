class Worker:
    def __init__(self,name,surname,rate,days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days

    def get_salary(self):
        print(self.days * self.rate)

worker_one = Worker("Иван","Иванович",2.3,30)
worker_one.get_salary()