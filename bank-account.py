import uuid
import datetime
import os


class BankAccount:
    def __init__(self, username, accountType, balance=0.0):
        # Assign initial values
        self.username = username
        self.accountType = accountType.lower()
        self.balance = balance

        # Generate a unique ID for each user
        self.userID = str(uuid.uuid4())[:8]  # short unique ID

        # Create a statement file for the account
        self.filename = f"{self.username}_{self.accountType}_{self.userID}.txt"

        # Initialize the statement file
        with open(self.filename, 'w') as file:
            file.write(f"Account Statement for {self.username} ({self.accountType.capitalize()})\n")
            file.write(f"Account ID: {self.userID}\n")
            file.write(f"Opening Balance: ${self.balance:.2f}\n")
            file.write("-" * 40 + "\n")

    # Deposit function
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return

        self.balance += amount
        self._record_transaction("Deposit", amount)
        print(f"${amount:.2f} deposited successfully. New balance: ${self.balance:.2f}")

    # Withdraw function
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

        if amount > self.balance:
            print("Insufficient balance for this withdrawal.")
            return

        self.balance -= amount
        self._record_transaction("Withdrawal", -amount)
        print(f"${amount:.2f} withdrawn successfully. New balance: ${self.balance:.2f}")

    # Get balance
    def get_balance(self):
        return self.balance

    # Get user ID
    def get_userID(self):
        return self.userID

    # Get username
    def get_username(self):
        return self.username

    # Get account type
    def get_accountType(self):
        return self.accountType

    # Record transaction in file
    def _record_transaction(self, transaction_type, amount):
        with open(self.filename, 'a') as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} | {transaction_type:<10} | {amount:>8.2f} | Balance: ${self.balance:.2f}\n")

    # Get transaction history
    def get_transaction_history(self):
        if not os.path.exists(self.filename):
            print("No transaction file found.")
            return []

        with open(self.filename, 'r') as file:
            history = file.readlines()

        return history


# --------------------------
# TESTING THE IMPLEMENTATION
# --------------------------
if __name__ == "__main__":
    # Create multiple accounts
    acc1 = BankAccount("Alice", "Checking", 500)
    acc2 = BankAccount("Bob", "Saving")

    # Perform transactions
    acc1.deposit(200)
    acc1.withdraw(100)
    acc2.deposit(1000)
    acc2.withdraw(300)
    acc2.withdraw(800)  # Should show insufficient balance

    # Print balances
    print("\nAccount Balances:")
    print(f"{acc1.get_username()} ({acc1.get_accountType()}): ${acc1.get_balance():.2f}")
    print(f"{acc2.get_username()} ({acc2.get_accountType()}): ${acc2.get_balance():.2f}")

    # Show transaction history for one user
    print("\nTransaction History for Alice:")
    for line in acc1.get_transaction_history():
        print(line.strip())
