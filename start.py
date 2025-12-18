# class Student:
#     def introduce(self, name, age, grade):
#         print(f"My name is {name}. I am {age} years old, and my grade is {grade}.")

# student1 = Student()
# student2 = Student()
# student3 = Student()

# student1.introduce("Yoq", 12, "3")
# student2.introduce("Yoq", 12, "3")
# student3.introduce("Yoq", 12, "11")




# class someCar:
#     def isdriving(self, color, brand):
#         print(f"The {color} {brand} is rolling over Tashkent!")

# someCar1 = someCar()
# someCar2 = someCar()
# someCar3 = someCar()

# someCar1.isdriving("Gold", "Li9")
# someCar2.isdriving("White", "Tracker")
# someCar3.isdriving("Pink", "Matiz")



# ●Create a BankAccount class with attributes account_number and balance.
# ●Add methods:
# ○deposit(amount) → increases balance.
# ○withdraw(amount) → decreases balance if enough funds.
# ○check_balance() → prints balance.
# ●Create two accounts and simulate transactions




# class Constructor:
#     def __init__(self, length, width):
#         self.length = length
#         self.width = width

#     def area(self):
#         return self.length * self.width

#     def perimeter(self):
#         return 2 * (self.length + self.width)
    
# rect1 = Constructor(12, 5)

# print("Area is:", rect1.area())
# print("Perimeter is:", rect1.perimeter())




# class ElectroBill:
#     def __init__(self, kilovatt):
#         self.kilovatt = kilovatt

#     def calculate_bill(self):
#         if self.kilovatt <= 200:
#             bill = self.kilovatt * 650
#         elif self.kilovatt <= 400:
#             bill = 200*650+ (self.kilovatt-200) * 950
#         elif self.kilovatt <= 500:
#             bill = 200*650 + 200*950 + (self.kilovatt - 400) * 1200
#         else:
#             bill = 200*650 + 200*950 + (self.kilovatt - 400) * 1200
#             discount = bill * 10 / 100
#             bill -= discount
#         return bill

# kilovatt_used = int(input("Please enter your electricity usage in this month: "))
# bill = ElectroBill(kilovatt_used)
# print("Total price is:", bill.calculate_bill(), "sum")





# def smth(a, b):
#     position = 0
#     how_many_b = 0
#     while position + b <= a:
#         position += b
#         how_many_b += 1
#     print(f"In {a} we can put {how_many_b}")
# smth(10, 3)




# class Product:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price

#     def discount(self, percentage):
#         price_after_disc = self.price * percentage / 100
#         self.price -= price_after_disc
#         print(f"Price of {self.name} after {percentage}% discount is => {self.price}")
#     def tax(self, percentage):
#         price_after_tax = self.price * percentage / 100
#         self.price += price_after_tax
#         print(f"Price of {self.name} after {percentage}% tax is => {self.price}")

# p = Product("Bread", 3000)
# p.tax(12)




# class Product:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price
# class Warehouse:
#     def __init__(self):
#         self.storage = []
#     def add_product(self, product, quantity):
#         self.storage.append((product, quantity))
#     def show_product(self):
#         for product, quantity in self.storage:
#             print(f"{product.name}: {quantity} pcs - ${product.price} each")
#     def all_prices(self):
#         total = 0
#         for product, qauntity in self.storage:
#             total += product.price * qauntity
#         print(f"All prices for all product is ${total}")

# tv = Product("TV", 450)
# apple = Product("Apple", 0.1)
# something = Product("Some", -1)

# warehouse = Warehouse()
# warehouse.add_product(tv, 50)
# warehouse.add_product(apple, 100)
# warehouse.add_product(something, 40)
# warehouse.show_product()
# warehouse.all_prices()





# class Animal:
#     def eat():
#         print("Animal is eating!")
#     def sleep():
#         print("Animal is sleeping!")

# class Dog(Animal):
#     def barking():
#         print("Dog is barking loudly!")
#     def eat():
#         print("Dog is eating it's food!")
#     def sleep():
#         print("Dog is sleeping peacefully!")
# class Camel(Animal):
#     def eat():
#         print("Camel is eating it's food!")
#     def drink():
#         print("Camel is drinking it's water!")
#     def sleep():
#         print("Camel is sleeping peacefully!")

# dog = Dog()
# camel = Camel()

# dog.barking()
# dog.eat()
# dog.sleep()

# camel.eat()
# camel.drink()
# camel.sleep()




# class Employee:
#     def __init__(self, name, base_salary):
#         self.name = name
#         self.base_salary = base_salary

#     def calculate_salary(self):
#         return self.base_salary

# class Full(Employee):
#     def calculate_salary(self):
#         return self.base_salary * 3

# class Part(Employee):
#     def calculate_salary(self):
#         return self.base_salary * 1.5

# class Intern(Employee):
#     def calculate_salary(self):
#         return self.base_salary * 0.5

# full_emp = Full("Someone1", 1000)
# part_emp = Part("Someone2", 1000)
# int_emp = Intern("Someone3", 1000)

# print(full_emp.name, "salary:", full_emp.calculate_salary())
# print(part_emp.name, "salary:", part_emp.calculate_salary())
# print(int.name, "salary:", int_emp.calculate_salary())




# class MyClass: # Creating great class
#     x = 5 # Saying x is 5
# p1 = MyClass() # Creating instance(Object) called p1
# print(p1.x) # Now we are using that Obecjt to print 5

        


# class Person:   # We created a class called person
#     def __init__(self, name, age): # Creating function to use __init__ wisely
#         self.name = name # This is needed to each object to hold different data init
#         self.age = age # Similar to previous one

# p1 = Person("Abdulaziz", 19) # Creating object
# p2 = Person("Aziz", 15) # Another object

# print(p2.age)
# print(p1.name)




# class Person:
#     def __init__(self, name, age = 22):
#         self.name = name
#         self.age = age
# person1 = Person("Hasan")
# person2 = Person("Husan", 19)

# print(person1.name, person1.age)
# print(person2.name, person2.age)





# class Account:
#     def __init__(self, balance = 0):
#         self.balance = balance

#     def deposit(self, amount):
#         self.balance += amount
#     def withdraw(self, amount):
#         self.balance -= amount
#     def display_balance(self):
#         print(f"Your balance is: {self.balance}")

# class SavingsAccount(Account):
#     withdraw_limit = 3
#     def __init__(self, balance = 0, withdraw_limit = 3):
#         super().__init__(balance)
#         self.withdraw_limit = withdraw_limit
#     def withdraw(self, amount):
#         if self.withdraw_limit <= 0:
#             print("Today's limit is reached!!!")
#             return
#         super().withdraw(amount)
#         self.withdraw_limit -= 1
#         print(f"Your {amount} amount of withfraw completed. Remaining limit is {self.withdraw_limit}")


# aziz_acc = SavingsAccount(800)

# aziz_acc.withdraw(110)
# aziz_acc.withdraw(90) 
# aziz_acc.withdraw(300)
# aziz_acc.withdraw(100)
# aziz_acc.display_balance()



# class Assignment:
#     def __init__(self, name, mark):
#         self.mark = mark
#         self.name = name
#     def grade(self):
#         if self.mark >= 90:
#             return "Distinction"
#         elif self.mark >= 60:
#             return "Merit"
#         elif self.mark >= 30:
#             return "Pass"
#         else:
#             return "Resubmission"
#     def display(self):
#         print(f"Student {self.name}, he got {self.mark} his grade was {self.grade()}")
    
# student1 = Assignment("Abdulaziz", 78)
# student2 = Assignment("Doston", 39)
# student3 = Assignment("Shoxruh", 60)

# student1.display()
# student2.display()
# student3.display()


# class Movie:
#     def __init__(self, name, seats=40):
#         self.name = name
#         self.seats = [True] * seats

#     def show_seats(self):
#         for i, available in enumerate(self.seats, 1):
#             print("💺" if available else "❌", end=" ")
#             if i % 10 == 0:
#                 print()

# class BookingSystem:
#     def __init__(self, movie, seat_price=1000):
#         self.movie = movie
#         self.seat_price = seat_price
#         self.balance = 0

#     def book(self, seat_number, user):
#         if self.movie.seats[seat_number - 1]:
#             if user.balance >= self.seat_price:
#                 self.movie.seats[seat_number - 1] = False
#                 user.balance -= self.seat_price
#                 self.balance += self.seat_price
#                 print(f"Seat {seat_number} booked {user.name}'s remaining balance is: {user.balance}")
#             else:
#                 print(f"{user.name} need to deposit some money to get {seat_number}")
#         else:
#             print(f"Seat {seat_number} not available")

#     def cancel(self, seat_number, user):
#         if not self.movie.seats[seat_number - 1]:
#             self.movie.seats[seat_number - 1] = True
#             user.balance += self.seat_price
#             self.balance -= self.seat_price
#             print(f"Seat {seat_number} canceled")
#         else:
#             print(f"Seat {seat_number} was already free")

# class User:
#     def __init__(self, name, balance=500):
#         self.name = name
#         self.balance = balance

#     def book_seat(self, book_system, seat_number):
#         book_system.book(seat_number, self)

#     def cancel_seat(self, book_system, seat_number):
#         book_system.cancel(seat_number, self)

# movie = Movie("1 Billion Dollar Movie")
# book_system = BookingSystem(movie, seat_price=1000)
# user = User("Palonchiev", balance=3000)

# user.book_seat(book_system, 5)
# movie.show_seats()




# class Book:
#     def __init__(self, title, author, pages=40, current_page = 0):
#         self.title = title
#         self.author = author
#         self.pages = pages
#         self.current_page = current_page
#     def read_page(self):
#         if self.pages > self.current_page:
#             self.current_page += 1
#             return f"You've read {self.current_page} page. {self.current_page}/{self.pages}"
#         else:
#             return "You've read all pages, move on to the new book!"
#     def show_current_page(self):
#         return f"{self.current_page} pages are done!"
# some_book = Book("American Love", "Palonchi")
# print(some_book.read_page())
# print(some_book.read_page())
# print(some_book.read_page())
# print(some_book.read_page())
# print(some_book.current_page)


# class Dog:
#     species = "Canis familiaris"
#     def __init__(self, name, age, energy=100):
#         self.name = name
#         self.age = age
#         self.energy = energy
#     def bark(self):
#         if self.energy <= 100:
#             self.energy -= 5
#             return f"{self.name}, said Woof! woof! and his energy is decreased by 5, remaining energy is {self.energy}"
#         else:
#             f"{self.name} is tired!"
# beagle = Dog("Beagle", 4)
# chihuahua = Dog("Chihuahua", 2)
# chihuahua = Dog("Chihuahua", 2)
# print(beagle.bark())
# print(chihuahua.bark())
# print(chihuahua.bark())




# class Bank:
#     def __init__(self, owner, balance=0):
#         self.owner = owner
#         self.balance = balance
#     def deposit(self, amount):
#         if amount > 0:
#             self.balance += amount
#         else:
#             return "Depositing negative number into balance is not possible!"
#     def withdraw(self, amount):
#         if amount > 0:
#             self.balance -= amount
#         else:
#             return "Withdrawing negative number into balance is not possible!"
#     def show_balance(self):
#         return f" Dear {self.owner}, you have {self.balance} sum on your balance!"

# some_owner1 = Bank(owner="Abdulaziz")
# some_owner2 = Bank(owner="Komiljon")

# some_owner1.deposit(5000)
# some_owner2.deposit(3000)
# some_owner1.withdraw(500)
# some_owner2.withdraw(1000)
# print(some_owner2.show_balance())
# print(some_owner1.show_balance())




#Make a Student class with class attribute
#school = "MidCoder Academy" and instance
#attributes: name, grades (empty list).
#Add method add_grade(score) that appends to grades.




# class Student:
#     school = "MidCoder Academy"

#     def __init__(self, name, grades = None):
#         if grades is None:
#             grades = []
#         self.grades = grades
#         self.name = name
#     def add_grade(self, score):
#         if score > 0:
#             self.grades.append(score)
#         else:
#             print("Cannot add negative score to a student!")
#     def print_grade_of_student(self):
#         if not self.grades:
#             print(f"Student {self.name} has no any grade!")
#         else:
#             print(f"Student {self.name} has {self.grades} grade at all!")

# student1 = Student("Abdulaziz")

# student1.add_grade(15)
# student1.print_grade_of_student()




#Create a Car class with class attribute wheels = 4 and instance
#attributes: make, model, fuel_level (0-100). Add method drive(distance)
#that reduces fuel_level by distance//10 (integer division).


# class Car:
#     wheels = 4
#     def __init__(self, model, fuel_level = 100):
#         self.model = model
#         self.fuel_level = fuel_level
#     def drive(self, distance):
#         if self.fuel_level > 0:
#             fuel_used = distance // 10
#             self.fuel_level -= fuel_used
#             print(f"Your {self.model} passed {distance} and used {fuel_used} litres of fuel for this ride!")
#         else:
#             print(f"You ran out of fuel, you need to go to Gas station asap!")
#     def show_fuel(self):
#         if self.fuel_level > 0:
#             print(f"Your {self.model} has {self.fuel_level} litres of fuel!")
#         else:
#             print(f"Your {self.model} has no fuel at all!")
# chevy = Car("Matiz")
# chevy.drive(100)
# chevy.show_fuel()




#Make a Coffee class with instance attributes: size
#("small"/"medium"/"large"), shots (default 2), milk
#(default False). Add method drink() that prints
#"sip sip" and reduces shots by 1.


# class Coffee:
#     def __init__(self, size, shots = 2, milk = False):
#         self.milk = milk
#         self.size = size
#         self.shots = shots
#     def drink(self):
#         if self.shots > 0:
#             self.shots -= 1
#             if self.milk == True:
#                 print("Creamy sip, because you ordered milky one!")
#             else:
#                 print(f"Sip, sip! {self.shots} left only!")
#         else:
#             print("No shots left!")

# coffee1 = Coffee("Medium", shots=3, milk=True)
# coffee1.drink()
# coffee1.drink()
# coffee1.drink()




#Create a Playlist class with instance attributes: name, songs
#(empty list), current_song_index (0). Add methods add_song(title)
#and next_song() that changes current_song_index (loop back to 0 if end).


# class Playlist:
#     def __init__(self, name, songs=None, current_song_index = 0):
#         if songs is None:
#             songs = []
#         self.songs = songs
#         self.name = name
#         self.current_song_index = current_song_index
#     def add_song(self, title):
#         self.songs.append(title)
#         print(f"{title} song is added now!")
#     def next_song(self):
#         if self.songs:
#             for i in range(len(self.songs)):
#                 print(self.songs[i])
#                 self.current_song_index = i
#         else:
#             print("List is empty!")
# new_song = Playlist("The Weeknd")
# new_song.add_song("Call out name")




#Make a Laptop class with class attribute os = "Linux (because you're based)"
#and instance attributes: brand, ram_gb, is_on (False). Add methods turn_on()
#and turn_off() that actually flip is_on.




# def filter_positive(nums):
#     res = []
#     for i in range(len(nums)):
#         if nums[i] > 0:
#             res.append(nums[i])
#         else:
#             pass
#     return res




# class Animal:
#     def speak(self):
#         print("General sound of an animal")

# class Dog(Animal):
#     def speak(self):
#         print("Woof")

# class Cat(Animal):
#     def speak(self):
#         print("Meow")

# class Sheep(Animal):
#     def speak(self):
#         print("Baa")

# def make_animal_speak(Animal):
#     Animal.speak()

# animals = [Dog(), Cat(), Sheep()]

# for a in animals:
#     make_animal_speak(a)



#Make a Laptop class with class attribute os =
#"Linux (because you're based)" and instance
#attributes: brand, ram_gb, is_on (False).
#Add methods turn_on() and turn_off() that actually flip is_on.


# class Laptop:
#     os = "Linux"
#     def __init__(self, brand, ram_gb, is_on = False):
#         self.brand = brand
#         self.ram_gb = ram_gb
#         self.is_on = is_on
#     def turn_on(self):
#         if self.is_on == False:
#             self.is_on = True
#             print(f"Welcome, your {self.brand} laptop is on now!")
#         else:
#             print("Your Laptop is already on!")
#     def turn_off(self):
#         if self.is_on == True:
#             self.is_on = False
#             print(f"Turning off the laptop!")
#         else:
#             print("Laptop is already sleeping!")
# ubuntu = Laptop("Lenovo", 8)
# ubuntu.turn_off()



#Create a Person class with instance attributes: name, money.
#Create a separate Shop class with class attribute items =
#{"apple": 1, "banana": 2, "gpu": 2000}. Add method buy(person,
#item_name) to Shop that checks if person has enough money and transfers it if yes.



# class Person:
#     def __init__(self, name, money):
#         self.name = name
#         self.money = money
# class Shop:
#     items = {"apple": 1000, "banana": 2000, "gpu": 4000}
#     @classmethod
#     def buy(cls, person, item_name):
#         if item_name not in cls.items:
#             print(f"{item_name} is not available in this shop!")
#             return
#         price = cls.items[item_name]
#         if person.money >= price:
#             person.money -= price
#             print(f"{person.name} bought {item_name} for {price}. Remaining money: {person.money}!")
#         else:
#             print(f"{person.name}, you have no money to buy {item_name}. I think you're broke by nature!")
    
# chunga = Person("Chunga", 500)
# changa = Person("Changa", 5000)
# shop = Shop()
# shop.buy(chunga, "apple")
# shop.buy(changa, "gpu")




# class Car:
#     def drive(self):
#         print("Car is moving...")
#     def analog_gauge():
#         print("We have some fuel")
# class ElectricCar(Car):
#     def __init__(self):
#         self.battery_percentage = 100
#     def drive(self):
#         if self.battery_percentage > 0:
#             self.battery_percentage -= 10
#             print("You driving, so I'll spend 10 percent of battery!")
#         else:
#             print("You're already run out of battery!")
#     def analog_gauge(self):
#         print(f"You have {self.battery_percentage} percent battery left!")

# class DieselCar(Car):
#     def __init__(self):
#         self.fuel_percentage = 100
#     def drive(self):
#         if self.fuel_percentage > 0:
#             self.fuel_percentage -= 10
#             print("You riving, so I will use 10 litres of fuel!")
#         else:
#             print("You have no fuel left!")
#     def analog_gauge(self):
#         print(f"You have {self.fuel_percentage} litres of fuel left!")

# leapmotor = ElectricCar()
# leapmotor.drive()
# leapmotor.analog_gauge()



#Payment hierarchy
#Base class Payment with method process().
#Subclasses: CreditCardPayment, PayPalPayment, CryptoPayment.
#Each prints different fee and confirmation message, but you
#process them in a loop without knowing type.



# class Payment:
#     def __init__(self, amount):
#         self.amount = amount

#     def process(self):
#         print("Proccessing something!")


# class CreditCardPayment(Payment):
#     def __init__(self, amount):
#         self.amount = amount

#     def process(self):
#         fee = self.amount * 0.01
#         total_charge = self.amount + fee
#         print(f"Credit car payment of {self.amount} has been proccessed. Fee: {fee}. Total charged: {total_charge}")

# class PaypalPayment(Payment):
#     def __init__(self, amount):
#         self.amount = amount

#     def process(self):
#         fee = self.amount * 0.03
#         total_charge = self.amount + fee
#         print(f"Paypal payment of {self.amount} has been proccessed. Fee: {fee}. Total charged: {total_charge}")

# class CryptoPayment(Payment):
#     def __init__(self, amount):
#         self.amount = amount
    
#     def process(self):
#         fee = self.amount * 0.0125
#         total_charge = self.amount + fee
#         print(f"Crypto payment for {self.amount} has been proccessed. Fee: {fee}. Total charge is {total_charge}. Payment confirmed by blockchain!")

# payments = [
#     CreditCardPayment(4000),
#     PaypalPayment(900),
#     CryptoPayment(7000)
# ]

# for payment in payments:
#     payment.process()




#Employee salary system
#Employee → base with calculate_salary().
#Subclasses: HourlyEmployee (hours × rate),
#SalariedEmployee (fixed), Manager (fixed + bonus).
#Company has list[Employee], loop and pay everyone correctly.
#Weapon system (you’ll love/hate this)

# class Employee:
#     def __init__(self, name):
#         self.name = name

#     def calculate_salary(self):
#         return 0

# class HourlyEmployee:
#     def __init__(self, hours, rate):
#         self.hours = hours
#         self.rate = rate
#         super()

#     def calculate_salary(self):
#         tot = self.hours * self.rate
#         print(f"Salary for {self.name}")
# class SalariedEmployee:
#     pass

# class Manager:
#     pass



# from abc import ABC, abstractmethod

# class Vehicle(ABC):
#     @abstractmethod
#     def calculate_rental_cost(self, days):
#         pass
#     def __init__(self, brand, daily_cost):
#         self.brand = brand
#         self.daily_cost = daily_cost
#         self.is_rented = False
#     def rent(self, days):
#         if self.is_rented:
#             print(f"{self.brand} is already rented by other person!")
#         else:
#             self.is_rented = True
#             cost = self.calculate_rental_cost(days)
#             print(f"You rented {self.brand} for {days} days. Price is {cost:,} sums")
#     def return_vehicle(self):
#         if self.is_rented:
#             self.is_rented = False
#             print(f"You returned {self.brand}. Thank you!")
#         else:
#             print(f"{self.brand} was not rented!")

# class Car(Vehicle):
#     insurance_fee = 5000
#     def __init__(self, brand, daily_cost = 1_000_000):
#         super().__init__(brand, daily_cost)

#     def calculate_rental_cost(self, days):
#         return self.daily_cost * days + self.insurance_fee
    
# class Bike(Vehicle):
#     def __init__(self, brand, daily_cost = 700_000):
#         super().__init__(brand, daily_cost)
#     def calculate_rental_cost(self, days):
#         return self.daily_cost * days
    
# class Truck(Vehicle):
#     def __init__(self, brand, max_weight, price_per_ton = 40_000, daily_cost = 3_000_000):
#         super().__init__(brand, daily_cost)
#         self.price_per_ton = price_per_ton
#         self.max_weight = max_weight
#     def calculate_rental_cost(self, days):
#         return self.daily_cost * days + self.max_weight * self.price_per_ton
    

# Lamborghini = Car("Lamborghini")
# matiz = Car("Matiz")
# bike = Bike("Yamaha")
# kamaz = Truck("KamAZ", max_weight=25)

# fleet = [Lamborghini, matiz, bike, kamaz]

# for v in fleet:
#     v.rent(5)














# dict1 = {"a": 1, "b": 2, "c": 3}
# dict2 = {"a": 2, "b": 5, "d": 3}
# dict3 = (dict1 | dict2)
# print(dict3)



# lst1 = [1, 3, 5, 7, 9]
# lst2 = [2, 4, 6, 8]
# for i in range(len(lst1)):
#     lst2.append(lst1[i])
# lst2.sort()
# print(lst2)






# def moveZeroes(nums):
#     left, right = 0, 1
#     for right in range(len(nums)):
#         if nums[right] != 0:
#             nums[left], nums[right] = nums[right], nums[left]
#             left += 1
#     return nums
# print(moveZeroes([1, 0, 2, 0, 0, 5, 12]))





# def removeDuplicates(nums):
#     if not nums:
#         return "No elements in the list"
    
#     slower = 0

#     for faster in range(1, len(nums)):
#         if nums[faster] != nums[slower]:
#             slower += 1
#             nums[slower] = nums[faster]
#     return slower + 1

# print(removeDuplicates([1,1,2,3,4,5,6,7,8,9]))



# def plusone(digits):
#     digit_str = "".join(map(str, digits))

#     digit_int = int(digit_str) + 1

#     res_int = str(digit_int)

#     return [int(d) for d in res_int]

# print(plusone([1,2,3]))



# class Solution:
#     def isPowerOfTwo(self, n: int) -> bool:
#         if n > 0:
#             if n & (n-1) == 0:
#                 return True
#             else:
#                 return False
#         else:
#             return False