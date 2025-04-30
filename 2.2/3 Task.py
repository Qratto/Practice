class Numbers:
    def __init__(self,num_one,num_two):
        self.num_one = num_one
        self.num_two = num_two

    def print_numbers(self):
        print(self.num_one,self.num_two)

    def set_number_one(self,new_num):
        self.num_one = new_num

    def set_number_two(self, new_num):
        self.num_two = new_num

    def sum_numbers(self):
        print("Сумма чисел: ",self.num_one + self.num_two)

    def finding_largest(self):
        if self.num_one > self.num_two:
            print(f"{self.num_one} больше чем {self.num_two}")
        elif self.num_one < self.num_two:
            print(f"{self.num_two} больше чем {self.num_one}")
        else:
            print("Числа равны")

object_class = Numbers(4,2)
object_class.print_numbers()
object_class.finding_largest()
object_class.sum_numbers()
object_class.set_number_two(6)
object_class.print_numbers()
object_class.finding_largest()