import importlib
import os
import sys
from typing import List, Dict, Optional


def task1():
    print("Завдання 1: Обробка виключень")

    def calc(a, b):
        try:
            x = float(a)
            y = int(b)
            res = x / y
            print("Результат ділення:", res)
        except (ValueError, ZeroDivisionError) as err:
            print("Помилка вводу або нуль:", err)

    def change_money(current, diff):
        try:
            val = float(diff)
            current = current + val
        except ValueError:
            print("Помилка: треба ввести число")
        else:
            print("Операція успішна, баланс:", current)
        finally:
            print("Блок finally: перевірку завершено")

    def read_file(name):
        try:
            with open(name, "r", encoding="utf-8") as target_file:
                data = target_file.read()
                print("Зміст файлу:", data)
        except FileNotFoundError:
            print("Файл не знайдено:", name)

    calc("500", "5")
    calc("abc", "5")
    calc("500", "0")

    change_money(1000, "200")
    change_money(1000, "текст")

    with open("temp.txt", "w", encoding="utf-8") as temp_file:
        temp_file.write("Дані рахунку: 12345")

    read_file("temp.txt")
    read_file("no_file.txt")


class AppError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return f"Помилка програми: {self.msg}"


class DataError(AppError):
    def __init__(self, field_name, val):
        self.field_name = field_name
        self.val = val
        super().__init__(f"Некоректні дані у полі {field_name}: {val}")


class MoneyError(AppError):
    def __init__(self, current, need):
        self.current = current
        self.need = need
        super().__init__(f"Не вистачає грошей: є {current}, треба {need}")


class AuthError(AppError):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"Користувача {user_id} не знайдено в базі")


def task2():
    print("Завдання 2: Власні класи помилок")

    def check_user(user_id):
        if user_id != "admin":
            raise AuthError(user_id)
        print("Доступ дозволено")

    def pay(balance, price):
        if price > balance:
            raise MoneyError(balance, price)
        return balance - price

    def parse_number(text):
        try:
            return int(text)
        except ValueError as err:
            raise DataError("вік", text) from err

    def logger_check(balance, price):
        try:
            pay(balance, price)
        except MoneyError:
            print("Лог: зафіксовано спробу списати більше ніж є")
            raise

    try:
        check_user("guest")
    except AuthError as e:
        print("Перехоплено AuthError:", e)

    try:
        pay(100, 500)
    except AppError as e:
        print("Перехоплено базовим AppError:", e)

    try:
        parse_number("двадцять")
    except DataError as e:
        print("Перехоплено:", e)
        print("Причина помилки (__cause__):", repr(e.__cause__))

    try:
        logger_check(50, 100)
    except MoneyError as e:
        print("Повторний raise спіймано у task2:", e)


def task3():
    print("Завдання 3: Модулі та пакети")

    os.makedirs("my_bank/models", exist_ok=True)
    os.makedirs("my_bank/utils", exist_ok=True)

    with open("my_bank/__init__.py", "w", encoding="utf-8") as init_file:
        init_file.write('__all__ = ["calc_tax"]\n')
        init_file.write('def calc_tax(x):\n    return x * 0.05\n')
        init_file.write('def hidden_func():\n    return "секрет"\n')

    with open("my_bank/models/__init__.py", "w", encoding="utf-8") as models_init:
        models_init.write("")

    with open("my_bank/models/user.py", "w", encoding="utf-8") as user_file:
        user_file.write('class User:\n    def __init__(self, name):\n        self.name = name\n')

    with open("my_bank/utils/__init__.py", "w", encoding="utf-8") as utils_init:
        utils_init.write("")

    with open("my_bank/utils/helpers.py", "w", encoding="utf-8") as helpers_file:
        helpers_file.write('def format_money(val):\n    return f"{val} грн"\n')

    if "." not in sys.path:
        sys.path.insert(0, ".")

    my_bank = importlib.import_module("my_bank")
    user_mod = importlib.import_module("my_bank.models.user")
    helpers_mod = importlib.import_module("my_bank.utils.helpers")

    User = getattr(user_mod, "User")
    format_money = getattr(helpers_mod, "format_money")

    u = User("Олексій")
    tax = my_bank.calc_tax(1000)
    formatted = format_money(tax)

    print("Користувач:", u.name)
    print("Податок:", formatted)
    print("Список __all__ у пакеті my_bank:", my_bank.__all__)


def task4():
    print("Завдання 4: Документування та інтроспекція")

    def register_client(name: str, age: int, cards: List[str]) -> Dict[str, Optional[str]]:
        """Реєструє клієнта у системі банку.

        Args:
            name: Ім'я клієнта.
            age: Вік клієнта.
            cards: Список номерів карток.

        Returns:
            Словник з даними клієнта.

        Raises:
            ValueError: Якщо вік менший за 18.
        """
        if age < 18:
            raise ValueError("Клієнт має бути повнолітнім")
        return {"name": name, "first_card": cards[0] if cards else None}

    print("Назва функції (__name__):", register_client.__name__)
    print("Анотації типів (__annotations__):", register_client.__annotations__)
    print("Docstring функції (__doc__):", register_client.__doc__)
    print("Виклик help():")
    help(register_client)

if __name__ == "__main__":
    task1()
    print()
    task2()
    print()
    task3()
    print()
    task4()
