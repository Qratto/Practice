number_dict = {}
class Train:
    def __init__(self,locality,number_train,departure_time):
        self.locality = locality
        self.number_train = number_train
        self.departure_time = departure_time
        number_dict[f"{number_train}"] = [locality,departure_time]

    def print_train_information(self,number_train):
        pass

train_one = Train("Томск","777","13:00")
train_two = Train("Москва","123","12:10")
train_three = Train("Самара","520","17:50")
num = input("Введите номер поезда: ")
sel_train = number_dict.get(num)
if sel_train:
    print(f"Город {sel_train[0]} время {sel_train[1]}")
else:
    print("Введен не правельный номер поезда")
