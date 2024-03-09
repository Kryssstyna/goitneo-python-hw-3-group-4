from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY.")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            return str(e)

    def remove_phone(self, phone):
        try:
            self.phones.remove(Phone(phone))
        except ValueError:
            return "Phone number not found."

    def edit_phone(self, old_phone, new_phone):
        try:
            idx = self.phones.index(Phone(old_phone))
            self.phones[idx] = Phone(new_phone)
        except ValueError:
            return "Phone number not found."

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            return str(e)

    def find_phone(self, phone):
        try:
            idx = self.phones.index(Phone(phone))
            return str(self.phones[idx])
        except ValueError:
            return "Phone number not found."

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(map(str, self.phones))}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(map(str, self.phones))}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, "Record not found.")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            return "Record not found."

    def get_birthdays_per_week(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        birthdays_next_week = []
        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date().replace(year=today.year)
                if today <= bday <= next_week:
                    birthdays_next_week.append((record.name.value, bday.strftime('%d.%m')))
        return birthdays_next_week

    def __str__(self):
        return '\n'.join(map(str, self.data.values()))


def main():
    book = AddressBook()

    while True:
        command = input("Enter a command: ").strip().lower()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command.startswith("add"):
            try:
                _, name, phone = command.split()
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print("Contact added.")
            except ValueError:
                print("Invalid command format. Please enter 'add [name] [phone]'.")

        elif command.startswith("change"):
            try:
                _, name, old_phone, new_phone = command.split()
                record = book.find(name)
                if isinstance(record, Record):
                    result = record.edit_phone(old_phone, new_phone)
                    if result:
                        print(result)
                    else:
                        print("Phone number updated.")
                else:
                    print(record)
            except ValueError:
                print("Invalid command format. Please enter 'change [name] [old_phone] [new_phone]'.")

        elif command.startswith("phone"):
            try:
                _, name = command.split()
                record = book.find(name)
                if isinstance(record, Record):
                    print(record)
                else:
                    print(record)
            except ValueError:
                print("Invalid command format. Please enter 'phone [name]'.")

        elif command == "all":
            print(book)

        elif command.startswith("add-birthday"):
            try:
                _, name, birthday = command.split()
                record = book.find(name)
                if isinstance(record, Record):
                    result = record.add_birthday(birthday)
                    if result:
                        print(result)
                    else:
                        print("Birthday added.")
                else:
                    print(record)
            except ValueError:
                print("Invalid command format. Please enter 'add-birthday [name] [birthday]'.")

        elif command.startswith("show-birthday"):
            try:
                _, name = command.split()
                record = book.find(name)
                if isinstance(record, Record) and record.birthday:
                    print(f"{record.name.value}'s birthday: {record.birthday.value}")
                elif isinstance(record, Record) and not record.birthday:
                    print(f"{record.name.value} has no birthday recorded.")
                else:
                    print(record)
            except ValueError:
                print("Invalid command format. Please enter 'show-birthday [name]'.")

        elif command == "birthdays":
            birthdays_next_week = book.get_birthdays_per_week()
            if birthdays_next_week:
                print("Birthdays coming up next week:")
                for name, bday in birthdays_next_week:
                    print(f"{name}: {bday}")
            else:
                print("No birthdays coming up next week.")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
