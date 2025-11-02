import json
import os
from datetime import datetime


class Bank:
    def __init__(self):
        pass

class Client:
    def __init__(self, name, second_name, DOB, phone_number, email_login, password):
        self.name = name
        self.second_name = second_name
        self.DOB = DOB
        self.phone_number = phone_number
        self.email_login = email_login
        self.password = password

class Account:
    pass

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

    Client_new = Client(name, second_name, DOB, phone_number, email_login, password)

    save_client(Client_new)
    print("You are registered! Welcome to Bank System!")
elif choice == "login":
    email_login = input("Enter your Email: ")
    password = input("Enter your Password: ")

    try:
        with open("Bank.json", "r") as file:
            clients = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        clients = []

    found = False
    for client in clients:
        if client["email_login"] == email_login and client["password"] == password:
            print(f"Welcome, {client['name']} {client['second_name']}!")
            found = True
            break

    if not found:
        print("Invalid login or password!")