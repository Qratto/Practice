string_one = input()
string_two = input()
count = 0
#Проверяем: если буквы одинаковые то прибавляем +1 в count
for i in range(len(string_one)):
    for j in range(len(string_two)):
        if string_one[i] == string_two[j]:
            count += 1
print(count)