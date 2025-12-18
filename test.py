class Employee:
    def init(self, ism, asosiy_maosh):
        self.ism = ism
        self.__asosiy_maosh = None
        self.maosh = asosiy_maosh

    @property
    def maosh(self):
        return self.__asosiy_maosh
    
    @maosh.setter
    def maosh(self, yangi_maosh):
        if yangi_maosh >= 1_000_000:
            self.__asosiy_maosh = yangi_maosh
        else:
            print("Maosh 1,000,000 dan kam bo'lishi mumkin emas!")
            self.__asosiy_maosh = 1_000_000

    def get_yearly_salary(self):
        return self.__asosiy_maosh * 12

    def bonus(self, foizi):
        return self.get_yearly_salary() * (foizi/ 100)


ishchi1 = Employee("Jasorat", 1_500_000)
print("Oy maoshi:", ishchi1.maosh)
print("Yillik maosh:", ishchi1.get_yearly_salary())
print("Bonus 10%:", ishchi1.bonus(10))


ishchi2 = Employee("Ali", 500_000)
print("Oy maoshi:", ishchi2.maosh)