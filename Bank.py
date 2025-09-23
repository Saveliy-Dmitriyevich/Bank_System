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
        if validation_func(value):
            return value
        else:
            print(error_message)

def validate_name(name):
    if not name or not name.isalpha() or len(name) >20:
        return False
    return True

def validate_dob(DOB):
    try:
        birth_date = datetime.strptime(DOB, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            return False
        return True
    except ValueError:
        return False

def validate_phone_number(phone_number):
    if not phone_number or not phone_number[1:].isdigit() or len(phone_number) != 13 or not phone_number.startswith("+375"):
        return False
    return True

def validate_email_login(email_login):
    if not email_login or not email_login.strip() or len(email_login) >20 or "@" not in email_login:
        return False
    local_part, dog, domain = email_login.partition("@")
    if len(local_part) < 3:
        return False
    if "." not in domain:
        return False
    with open("domain.txt", "r", encoding="utf-8") as f:
        valid_domains = set()
        for line in f:
            clean_domain = line.strip().lower()
            valid_domains.add(clean_domain)
    top_level_domain = domain.split(".")[-1].lower()
    if top_level_domain not in valid_domains:
        return False
    return True


print("Hello, it is our Bank system. Do you want to register or login?")
choice = input().strip().lower()

if choice == "register":
    name = input_with_validation('Hello, what is your name?', validate_name, "Please enter correct name: ")
    second_name = input_with_validation('What is your second name?', validate_name, "Please enter correct second name: ")
    DOB = input_with_validation('What is your Date of Birth?', validate_dob, "Please enter correct Date of Birth Use DD-MM-YYYY: ")
    phone_number = input_with_validation("enter your phone number: ", validate_phone_number, "Please enter correct phone number: ")
    email_login = input_with_validation("enter your email login: ", validate_email_login, "Please enter correct email login: ")
    password = input("Enter your Password: ")

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