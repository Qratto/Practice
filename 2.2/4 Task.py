class Counter:
    def __init__(self, count = 0):
        self.count = count

    def increase(self):
        self.count += 1
    def decrease(self):
        self.count -= 1


score_one = Counter()
score_two = Counter(10)
print(score_one.count)
print(score_two.count)
score_two.increase()
print(score_two.count)