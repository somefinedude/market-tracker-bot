
class BankAccount():
    def __init__(self, account_number, balance=0):
        self.__account_number = account_number
        self.__balance = balance

    def get_balance(self):
        return self.__balance
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance: {self.__balance}")
        else:
            print("Insufficient balance.")

    def get_account_number(self):
        return self.__account_number


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.05):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        max_withdrawable = self.get_balance() * 0.8
        if amount <= max_withdrawable:
            super().withdraw(amount)
        else:
            print(f"Cannot withdraw more than 80% of balance. Max allowed: {max_withdrawable}")

class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance=0, overdraft_limit=500):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= self.get_balance() + self.overdraft_limit:
            new_balance = self.get_balance() - amount
            self._BankAccount__balance = new_balance
            print(f"Withdrew {amount}. New balance: {self.get_balance()}")
        else:
            print(f"Cannot withdraw beyond overdraft limit ({self.overdraft_limit})")

def main():
    savings = SavingsAccount("SAV123", 1000)
    checking = CheckingAccount("CHK456", 500)

    accounts = [savings, checking]

    for account in accounts:
        print(f"\nAccount: {account.get_account_number()}, Balance: {account.get_balance()}")
        account.deposit(200)
        account.withdraw(1000)

main()
