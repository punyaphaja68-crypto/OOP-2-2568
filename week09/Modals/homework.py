class BankAccount:
    def __init__(self,balance):
        self.balance = balance

    def __sub__(self,other):
        if isinstance(other,BankAccount):
            new_account = new_balance = self.balance - other.balance
            new_account = BankAccount(new_balance)
            return new_account
        return None
    
    def __add__(self,other):
       if isinstance(self,other)
           new_balance = self.balance + other.balance
           new_account = BankAccount(new_balance)
           return new_account
    
    def __str__(self):
        return f"BankAccount: {self.balance:,.2f}"
