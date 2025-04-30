class Calculation:
    def __init__(self,calculation_line):
        self.__calculation_line = calculation_line


    def set_calculation_line(self,calculation_line):
        self.__calculation_line = calculation_line

    def set_last_symbol_calculation_line(self,symbol):
        self.__calculation_line = self.__calculation_line + symbol

    def get_calculation_line(self):
        return self.__calculation_line

    def get_last_symbol(self):
        return self.__calculation_line[-1]

    def delete_last_symbol(self):
        calculation_line_temporary = self.__calculation_line[:-1]
        self.__calculation_line = calculation_line_temporary


line = Calculation("Привет")
line.set_last_symbol_calculation_line("!")
print(line.get_calculation_line())
line.delete_last_symbol()
print(line.get_calculation_line())
line.delete_last_symbol()
print(line.get_calculation_line())
