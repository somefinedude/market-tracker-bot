class Iterator:
    def __init__(self):
        self.data = [1,2,3]
    def __iter__(self):
        self.index = 0
        return self
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration("TUGADI!")
        else:
            current_element = self.data[self.index]
            self.index += 1
            return current_element
y = Iterator()
a = iter(y)
print(next(a))
print(next(a))
print(next(a))
