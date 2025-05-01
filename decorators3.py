import csv
import re
from functools import wraps
from datetime import datetime
import os
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ

#Логер из дз Декораторы
def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        function_name = old_function.__name__
        date_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'Время вызова: {date_time}. Имя функции: {function_name}. '
                    f'Первый аргумент: {args}. Второй аргумент: {kwargs}. '
                    f'Результат: {result}\n')
        return result
    return new_function


# Функция для форматирования телефонных номеров
@logger
def format_phone(phone):
    phone = re.sub(r'\D', '', phone)  # Убираем все нецифровые символы
    if len(phone) == 11 and phone.startswith('7'):
        return f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    elif len(phone) == 10:
        return f"+7({phone[0:3]}){phone[3:6]}-{phone[6:8]}-{phone[8:]}"
    return phone


# Приводим данные к нужному формату
formatted_contacts = {}
for contact in contacts_list:
    # Обработка ФИО
    name_parts = contact[0].split()
    lastname = name_parts[0]
    firstname = name_parts[1] if len(name_parts) > 1 else ''
    surname = name_parts[2] if len(name_parts) > 2 else ''

    # Форматирование телефона
    phone = contact[5]
    formatted_phone = format_phone(phone)

    # Формируем уникальный ключ для группировки
    key = (lastname, firstname)

    # Если ключ уже есть, объединяем данные
    if key in formatted_contacts:
        existing_contact = formatted_contacts[key]
        existing_contact[3] = existing_contact[3] or contact[3]  # organization
        existing_contact[4] = existing_contact[4] or contact[4]  # position
        existing_contact[5] = formatted_phone  # phone
        existing_contact[6] = existing_contact[6] or contact[6]  # email
    else:
        formatted_contacts[key] = [lastname, firstname, surname, contact[3], contact[4], formatted_phone, contact[6]]

# Преобразуем словарь обратно в список
contacts_list = list(formatted_contacts.values())

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

# Выводим результирующий список для проверки
pprint(contacts_list)
