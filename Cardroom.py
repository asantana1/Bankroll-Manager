class Cardroom:
    def __init__(self, name, balance=0.0):
        self._name = name
        self._balance = balance
        self._transactions = []

    # Getter for name
    @property
    def name(self):
        return self._name

    # Getter and Setter for balance
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        self._balance = amount

    def deposit(self, amount, description="Deposit"):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._transactions.append((amount, description))

    def withdraw(self, amount, description="Withdrawal"):
        if amount <= 0 or amount > self._balance:
            raise ValueError("Invalid withdrawal amount")
        self._balance -= amount
        self._transactions.append((-amount, description))

    def get_transactions(self):
        return self._transactions
