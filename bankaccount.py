class BankAccount:
    def __init__(self,bank_account_number, account_holder, balance=0):
        self.bank_account_number = bank_account_number
        self.account_holder = account_holder
        self._balance = balance
   
    @property
    def balance(self):
        return self._balance
   
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
   
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
   
    def __str__(self):
        return f"{type(self).__name__}({self.bank_account_number}, {self.account_holder}, {self.balance})"

class SavingsAccount(BankAccount):
    def __init__(self, bank_account_number, account_holder, balance=0,
             interest_rate=0.01, minimum_balance=100):
        super().__init__(bank_account_number, account_holder, balance)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance  # Minimum balance requirement for savings account

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest

    def withdraw(self, amount):
        if amount > 0 and self._balance - amount < self.minimum_balance:
            raise ValueError("Cannot withdraw below minimum balance")
        super().withdraw(amount)
    
    def __str__(self) -> str:
        return f"{super().__str__()}, rate={self.interest_rate}"    
   
if __name__ == "__main__":
    # --- savings tests ---
    savings = SavingsAccount("002", "Schuja", 1000, 0.03)
    savings.add_interest()
    print(savings)                            # SavingsAccount(002, Schuja, 1030.0), rate=0.03

    try:
        savings.withdraw(2000)
    except ValueError as e:
        print("Error:", e)                    # Cannot withdraw below minimum balance

    print(isinstance(savings, BankAccount))   # True

    # --- menu loop ---
    acct = BankAccount("001", "Schuja")

    while True:
        choice = input("deposit / withdraw / quit: ").strip().lower()
        if choice == "quit":
            break

        try:
            amount = float(input("Enter amount: "))
            if choice == "deposit":
                acct.deposit(amount)
            elif choice == "withdraw":
                acct.withdraw(amount)
            else:
                print("Invalid choice")
            print(acct)
        except ValueError as e:
            print(f"Error: {e}")