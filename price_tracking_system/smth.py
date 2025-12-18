# class CustomDict:
#     def __init__(self):
#         self.data = {}
#     def __setitem__(self, key, value):
#         self.data[key]=value
    
#     def __getitem__(self, key):
#         return self.data[key]

#     def __str__(self):
#         return str(self.data)

# x = CustomDict()
# x["A"]=1
# print(x["A"])
# print(x)



# a = [1, 2, 3]
# b = iter(a)
# print(type(b))
# print(next(b))
# print(next(b))
# print(next(b))
# print(next(b))


# class CustomList:
#     def __init__(self):
#         self.lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     def __iter__(self):
#         return iter(self.lst)

# a = CustomList()
# print(dir(a))
# for i in a:
#     print(i)




# class Student:
#     def __hash__(self):
#         return None

# f = Student()
# s = tuple()
d = []
# # e = {}
# # a = {1: 1, "A": 2, s: 3, d: 4, e: 5, f: "O"}
# s = {f: 5}

# print(dir(f))
print(hash(d))