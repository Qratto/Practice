class MyClass:
    def __init__(self, params_one="default", params_two ="default"):
        self.property_one = params_one
        self.property_two = params_two
        print(f"Создан объект: {self.property_one}, {self.property_two}")

    def __del__(self):
        print(f"Удаление объекта: {self.property_one}, {self.property_two}")


object1 = MyClass()
object2 = MyClass("1")
object3 = MyClass("text", "3")

print()
del object1,object2,object3