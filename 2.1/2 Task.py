def combination(candidates, target):
    result = []
    candidates.sort()
    def backtrack(start, path, total):
        #Проверяем сумму: если сумма чисел больше или равна target
        if total == target:
            result.append(path.copy())
            return
        if total > target:
            return

        for i in range(start, len(candidates)):
            #Проверка на дубликаты,для этого в начане была сортировка
            if i > start and candidates[i] == candidates[i-1]:
                continue
            path.append(candidates[i])
            total += candidates[i]
            #Создаем рекурсию
            backtrack(i + 1, path, total)
            #Удадяем последний элемент и продолжаем перебор
            path.pop()
            total -= candidates[i]

    backtrack(0, [], 0)
    return result

candidates = [10,1,2,7,6,1,5]
target = 8
print(combination(candidates,target))
