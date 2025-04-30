class Worker:
    def __init__(self,name,surname,rate,days):
        self.__name = name
        self.__surname = surname
        self.__rate = rate
        self.__days = days

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_rate(self):
        return self.__rate

    def get_days(self):
        return self.__days

    def get_salary(self):
        print(self.__days * self.__rate)

worker_one = Worker("Иван","Иванович",2.3,30)
print(f"{worker_one.get_name()} \n"
      f"{worker_one.get_surname()} \n"
      f"{worker_one.get_rate()} \n"
      f"{worker_one.get_days()}")