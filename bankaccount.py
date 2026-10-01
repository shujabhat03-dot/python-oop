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
        return f"BankAccount({self.bank_account_number}, {self.account_holder}, {self.balance})"

acct = BankAccount("001", "Schuja")

while True:
    choice=input("deposit / withdraw / quit: ").strip().lower()
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