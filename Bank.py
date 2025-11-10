import json
import os
from datetime import datetime
from forex_python.converter import CurrencyRates, CurrencyCodes
import random


class Bank:
    def __init__(self, clients_file="Bank.json", accounts_file="Account.json"):
        self.clients_file = clients_file
        self.accounts_file = accounts_file
        self.clients = self.load_clients()
        self.accounts = self.load_accounts()

    def load_clients(self):
        if not os.path.exists(self.clients_file):
            return []
        try:
            with open(self.clients_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def load_accounts(self):  #делает переменную
        if not os.path.exists(self.accounts_file):
            return []
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_client(self, client):
        clients = self.load_clients()
        clients.append(client.__dict__)
        with open(self.clients_file, "w", encoding="utf-8") as f:
            json.dump(clients, f, indent=4, ensure_ascii=False)

    def save_account(self, account):
        accounts = self.load_accounts()
        accounts.append(account.__dict__)
        with open(self.accounts_file, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=4, ensure_ascii=False)

    def find_client_by_email(self, email):
        for c in self.clients:
            if c["email_login"] == email:
                return c
        return None

    def count_accounts_by_email(self, email):
        result = 0
        for acc in self.accounts:
            if acc["owner_email"] == email:
                result += 1
        return result

    def find_accounts_by_email(self, email):
        result = []
        for acc in self.accounts:
            if acc["owner_email"] == email:
                result.append(acc)
        return result

    def find_account_by_account_number(self, acc_num):
        result = []
        for acc in self.accounts:
            if acc['account_number'] == acc_num:
                result.append(acc)
        if len(result) == 0:
            return None
        else:
            return result

class Client:
    def __init__(self, name, second_name, DOB, phone_number, email_login, password, uni_number):
        self.name = name
        self.second_name = second_name
        self.DOB = DOB
        self.phone_number = phone_number
        self.email_login = email_login
        self.password = password
        self.uni_number = uni_number
        self.accounts = []  # список номеров счетов

    def add_account(self, account):
        self.accounts.append(account.account_number)

class Account:
    def __init__(self, account_number, owner_email, currency, balance=0.0):
        self.account_number = account_number
        self.owner_email = owner_email
        self.balance = float(balance)
        self.currency = currency
        self.history = []

    def show_balance(self, currency="BYN"):
        c = CurrencyRates()
        if currency == "BYN":
            print(f"Balance: {self.balance:.2f} BYN")
        else:
            try:
                rate = c.get_rate("BYN", currency)
                converted = self.balance * rate
                print(f"Balance: {converted:.2f} {currency}")
            except Exception as e:
                print(f"Error converting balance: {e}")

    def deposit(self, amount, currency):
        c = CurrencyRates()
        time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if currency != 'BYN':
            try:
                rate_to_byn = c.get_rate(currency, 'BYN')
                amount_byn = amount * rate_to_byn
            except Exception as e:
                print(f"Ошибка для {currency}: {e}")
                return
        else:
            amount_byn = amount

        self.balance += amount_byn
        self.history.append(f"{time_now}, Deposited {amount} {currency} ({amount_byn:.2f} BYN)")
        print("Deposit successful!")

    def withdraw(self, amount, currency):
        c = CurrencyRates()
        time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if currency != 'BYN':
            try:
                rate_to_byn = c.get_rate(currency, 'BYN')
                amount_byn = amount * rate_to_byn
            except Exception as e:
                print(f"Ошибка для {currency}: {e}")
                return
        else:
            amount_byn = amount

        if amount_byn > self.balance:
            print("Not enough funds.")
            return

        self.balance -= amount_byn
        self.history.append(f"{time_now}, You withdrew {amount} {currency} ({amount_byn:.2f} BYN)")
        print("Withdrawal successful!")

    def belarus_currency_rates(self):
        c = CurrencyRates()
        cc = CurrencyCodes()

        print("=== КУРСЫ БЕЛОРУССКОГО РУБЛЯ ===")
        print(f"Валюта: {cc.get_currency_name('BYN')} ({cc.get_symbol('BYN')})")
        print(f"Актуально на: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print()

        # Основные курсы
        currencies = ['USD', 'EUR', 'RUB', 'PLN', 'UAH']

        for curr in currencies:
            try:
                # Иностранная валюта к BYN
                rate_to_byn = c.get_rate(curr, 'BYN')
                # BYN к иностранной валюте
                rate_from_byn = c.get_rate('BYN', curr)

                print(f"1 {curr} = {rate_to_byn:.4f} BYN")
                print(f"1 BYN = {rate_from_byn:.4f} {curr}")
                print("-" * 30)

            except Exception as e:
                print(f"Ошибка для {curr}: {e}")

def uni_number_generation():
    return random.randint(1000000, 9999999)

def validation_uni_number(clients, uni_number_json):
    existing_numbers = set()
    for client in clients:
        if uni_number_json in client:
            existing_numbers.add(client[uni_number_json])

    while True:
        new_number = uni_number_generation()
        if new_number not in existing_numbers:
            uni_number = new_number
            break

    return uni_number

def save_client(client):
    filename = "Bank.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                clients = json.load(file)
            except json.JSONDecodeError:
                clients = []
    else:
        clients = []
    clients.append(client.__dict__)
    with open(filename, "w") as file:
        json.dump(clients, file, indent=4)

# ====================== ВАЛИДАЦИЯ ======================

def input_with_validation(prompt, validation_func, error_message):
    while True:
        value = input(prompt)
        result = validation_func(value)

        # Если функция возвращает (True/False, message)
        if isinstance(result, tuple):
            is_valid, message = result
        else:
            is_valid, message = result, error_message

        if is_valid:
            return value
        else:
            print(message)

def validate_name(name):
    if not name or not name.isalpha() or len(name) >20:
        return (False, 'Name must be at least 20 characters long and must to have only letters')
    return True

def validate_dob(DOB):
    try:
        birth_date = datetime.strptime(DOB, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return (False, 'You are older than 18 years :D')
        return True
    except ValueError:
        return False

def validate_phone_number(phone_number):
    if not phone_number or not phone_number[1:].isdigit() or len(phone_number) != 13 or not phone_number.startswith("+375"):
        return (False, 'The phone number must be in the form +375xxxxxxxxx')
    return True

def validate_email_login(email_login):
    if not email_login or not email_login.strip() or len(email_login) >30 or "@" not in email_login:
        return (False, 'email_login must be at least 30 characters long and must to have @')
    local_part, dog, domain = email_login.partition("@")
    if len(local_part) < 3:
        return (False, 'Your email must be in the form xxx@domain.xx')
    if "." not in domain:
        return (False, 'Your domain must have "." ')
    with open("domain.txt", "r", encoding="utf-8") as f:
        valid_domains = set()
        for line in f:
            clean_domain = line.strip().lower()
            valid_domains.add(clean_domain)
    top_level_domain = domain.split(".")[-1].lower()
    if top_level_domain not in valid_domains:
        return (False, 'Your domain does not exist')
    with open("Bank.json", "r") as file:
        clients = json.load(file)

        for client in clients:
            if client["email_login"] == email_login:
                return (False, 'This email already exists')
    return True

def validate_password(password, name, second_name, DOB, phone_number, email_login):
    feedback = []
    valid = True
    weak_passwords = ["123456", "password", "qwerty", "111111", "abc123"]
    # 1. Длина
    if 8 <= len(password) <= 30:
        feedback.append("✅ Length between 8 and 30 characters")
    else:
        feedback.append("❌ Password must be 8–30 characters long")
        valid = False
    # 2. Разные типы символов
    if any(c.isupper() for c in password):
        feedback.append("✅ Has uppercase letter")
    else:
        feedback.append("❌ Missing uppercase letter")
        valid = False
    if any(c.islower() for c in password):
        feedback.append("✅ Has lowercase letter")
    else:
        feedback.append("❌ Missing lowercase letter")
        valid = False
    if any(c.isdigit() for c in password):
        feedback.append("✅ Has number")
    else:
        feedback.append("❌ Missing number")
        valid = False
    if any(not c.isalnum() for c in password):
        feedback.append("✅ Has special character")
    else:
        feedback.append("❌ Missing special character")
        valid = False
    # 3. Проверка на слабый пароль
    if password.lower() in weak_passwords:
        feedback.append("❌ Password is too common")
        valid = False
    else:
        feedback.append("✅ Not a common password")
    # 4. Проверка на личную информацию
    if (
        name.lower() in password.lower()
        or second_name.lower() in password.lower()
        or DOB.replace("-", "") in password
        or phone_number in password
        or email_login.split("@")[0].lower() in password.lower()
    ):
        feedback.append("❌ Contains personal info")
        valid = False
    else:
        feedback.append("✅ No personal info")
    if valid == False:
        print("\n".join(feedback))
    return (valid, "Password check complete" if valid else "Password does not meet requirements")

def personal_account():
    pass

def Show_my_accounts():
    accounts = bank.find_accounts_by_email(email_login)
    if not accounts:
        print("You have no accounts.")
    else:
        for acc in accounts:
            print(f"• {acc['account_number']} | {acc['currency']} | {acc['balance']:.2f} {acc['currency']}")

# ====================== ОСНОВНАЯ ЛОГИКА ======================
bank = Bank()

print("Hello, it is our Bank system. Do you want to register or login?")
choice = input().strip().lower()

if choice == "register":
    name = input_with_validation('Hello, what is your name? ', validate_name, "Please enter correct name: ")
    second_name = input_with_validation('What is your second name? ', validate_name, "Please enter correct second name: ")
    DOB = input_with_validation('What is your Date of Birth? Please enter DOB in format DD-MM-YY! ', validate_dob, "Please enter correct Date of Birth Use DD-MM-YYYY: ")
    phone_number = input_with_validation("enter your phone number: ", validate_phone_number, "Please enter correct phone number: ")
    email_login = input_with_validation("enter your email login: ", validate_email_login, "Please enter correct email login: ")
    password = input_with_validation(
        "Enter your password: ",
        lambda p: validate_password(p, name, second_name, DOB, phone_number, email_login),
        "Invalid password"
    )
    clients = bank.clients
    uni_number_json = 'uni_number'
    uni_number = validation_uni_number(clients, uni_number_json)


    Client_new = Client(name, second_name, DOB, phone_number, email_login, password,uni_number)

    save_client(Client_new)
    print("You are registered! Welcome to Bank System!")
elif choice == "login":
    email_login = input("Enter your Email: ")
    password = input("Enter your Password: ")

    client = bank.find_client_by_email(email_login)
    if client  and client["password"] == password:

        print(f"Welcome, {client['name']} {client['second_name']}!")

        while True:
            print("\n\n\n\n\n\n\n--- Account Menu ---")
            print("1. Show my accounts")
            print("2. Create new account")
            print("3. Account replenishment")
            print("4. Withdraw money")
            print("5. Exchange rates")
            print("6. Exit")
            bank.accounts = bank.load_accounts()
            bank.clients = bank.load_clients()
            ch = input("Choose: ")

            if ch == "1":
                Show_my_accounts()

            elif ch == "2":
                if bank.count_accounts_by_email(email_login) == 3:
                    print('You have created all the accounts')
                    continue
                else:
                    currency = input("Enter currency (BYN/USD/EUR): ").upper()

                    if currency.upper() not in ["BYN", "USD", "EUR"]:
                        print("Invalid currency.")
                    else:
                        uni_account = bank.accounts
                        account_exists = False
                        for acc in bank.accounts:
                            if acc["owner_email"] == email_login and acc["currency"] == currency:
                                print('This account is already registered.')
                                account_exists = True
                                break

                        if not account_exists:
                            account_number = 'account_number'
                            acc_number = validation_uni_number(uni_account, account_number)
                            new_acc = Account(acc_number, email_login, currency, 0.0)
                            bank.save_account(new_acc)
                            print("✅ Account created successfully!")


            elif ch == "3": # Пополнение счета res[0]['balance']
                Show_my_accounts()
                uni_account = bank.accounts
                uni_client = bank.clients
                uni_number = int(input('Which account do you want to top up? '))
                currency = input("Enter currency (BYN/USD/EUR): ").upper()
                sum = int(input("Enter your sum: "))
                res = bank.find_account_by_account_number(uni_number)
                if res == None:
                    print("<UNK> Account does not exist.")
                    continue
                else:
                    pass
                    # Account.deposit(sum, currency)


            elif ch == "4": # Снять гроши
                pass

            elif ch == "5": # Курсы валют в БУН
                pass

            elif ch == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option!")

    else:
        print("❌ Invalid login or password.")