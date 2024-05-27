import random
import string

# Base class for an account
class Account:
    def __init__(self, account_number, balance=0, account_type="", password=""):
        self.account_number = account_number
        self.balance = balance
        self.account_type = account_type
        self.password = password

    # Method to check the balance of the account
    def check_balance(self):
        return self.balance

    # Method to deposit an amount into the account
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # Method to withdraw an amount from the account
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance -= amount
            return True

    # Method to transfer money to another account
    def transfer_money(self, recipient_account, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            return True

    # Method to delete the account
    def delete_account(self, accounts):
        accounts.remove(self)
        save_accounts_to_file(accounts)
        print(f"Account {self.account_number} deleted successfully.")

# Class for personal accounts, inherits from Account
class PersonalAccount(Account):
    def __init__(self, account_number, balance=0, password=""):
        super().__init__(account_number, balance, "Personal", password)

# Class for business accounts, inherits from Account
class BusinessAccount(Account):
    def __init__(self, account_number, balance=0, password=""):
        super().__init__(account_number, balance, "Business", password)

# Function to generate a random 10-digit account number
def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

# Function to create a new account
def create_account(account_type, initial_deposit=0):
    account_number = generate_account_number()
    # Loop to ensure the password is numeric
    while True:
        password = input("Set a numeric password for your account: ")
        if password.isdigit():
            break
        else:
            print("Password must be numeric. Please try again.")
    if account_type == "personal":
        return PersonalAccount(account_number, initial_deposit, password)
    elif account_type == "business":
        return BusinessAccount(account_number, initial_deposit, password)

# Function to log in to an existing account
def login(account_number, password):
    accounts = load_accounts_from_file()
    for account in accounts:
        if account.account_number == account_number and account.password == password:
            return account
    return None

# Function to save all accounts to a file
def save_accounts_to_file(accounts):
    with open("accounts.txt", "w") as file:
        for account in accounts:
            file.write(f"{account.account_number},{account.balance},{account.account_type},{account.password}\n")

# Function to load all accounts from a file
def load_accounts_from_file():
    accounts = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file.readlines():
                account_info = line.strip().split(",")
                account_type = account_info[2]
                if account_type == "Personal":
                    account = PersonalAccount(account_info[0], float(account_info[1]), account_info[3])
                elif account_type == "Business":
                    account = BusinessAccount(account_info[0], float(account_info[1]), account_info[3])
                accounts.append(account)
    except FileNotFoundError:
        pass
    return accounts

# Function to find an account by its number
def find_account_by_number(account_number, accounts):
    for account in accounts:
        if account.account_number == account_number:
            return account
    return None

# Main function to handle user interactions
def main():
    accounts = load_accounts_from_file()
    while True:
        action = input("Enter action (create, login, transfer, delete, exit): ").lower()
        if action == "create":
            account_type = input("Enter account type (personal/business): ").lower()
            initial_deposit = float(input("Enter initial deposit: "))
            new_account = create_account(account_type, initial_deposit)
            accounts.append(new_account)
            save_accounts_to_file(accounts)
            print(f"New account {new_account.account_number} created.")
        elif action == "login":
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            logged_in_account = login(account_number, password)
            if logged_in_account:
                print(f"Logged in to account {logged_in_account.account_number}.")
                # Add menu options for logged-in account
            else:
                print("Invalid credentials.")
        elif action == "transfer":
            sender_account_number = input("Enter sender account number: ")
            receiver_account_number = input("Enter receiver account number: ")
            amount = float(input("Enter transfer amount: "))
            sender_account = find_account_by_number(sender_account_number, accounts)
            receiver_account = find_account_by_number(receiver_account_number, accounts)
            if sender_account and receiver_account:
                if sender_account.transfer_money(receiver_account, amount):
                    save_accounts_to_file(accounts)
                    print("Transfer successful.")
                else:
                    print("Transfer failed.")
            else:
                print("Invalid account numbers.")
        elif action == "delete":
            account_number = input("Enter account number to delete: ")
            password = input("Enter password: ")
            account_to_delete = login(account_number, password)
            if account_to_delete:
                account_to_delete.delete_account(accounts)
            else:
                print("Invalid credentials or account not found.")
        elif action == "exit":
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()



