import os
import json
import re


class Records:
    """Класс для представления записей в телефонной книге."""
    def __init__(self,
                 last_name: str,
                 first_name: str,
                 middle_name: str,
                 organization: str,
                 work_phone: str,
                 personal_phone: str):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.middle_name}'
                f'Организация: {self.organization}'
                f'Рабочий телефон: {self.work_phone}'
                f'Личный телефон: {self.personal_phone}')


class PhoneBook:
    """Класс для представления телефонной книги и её функциональности."""
    def __init__(self, file: str):
        self.file = file
        self.records = self.load_data()

    def load_data(self) -> list[Records]:
        """Функция отвечающая за загрузку данных из файла."""
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Records(**entry_data) for entry_data in data]
        return []

    def save_data(self):
        """Сохраняет данные в файл."""
        data = [{'last_name': record.last_name,
                 'first_name': record.first_name,
                 'middle_name': record.middle_name,
                 'organization': record.organization,
                 'work_phone': record.work_phone,
                 'personal_phone': record.personal_phone}
                for record in self.records]
        with open(self.file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def validate_phone(self, prompt: str) -> str:
        """Валидация телефонных номеров."""
        while True:
            phone = input(prompt)
            if re.match(r'^\d{11}$', phone):
                return phone
            print('Некорректный формат номера телефона.')

    def result_print(self, index: int, record: Records):
        """Вывод данных."""
        print(f'{index}. {record.last_name}'
              f' {record.first_name} {record.middle_name}')
        print(f'   Организация: {record.organization}')
        print(f'   Рабочий телефон: {record.work_phone}')
        print(f'   Личный телефон: {record.personal_phone} \n')

    def input_record_fields(self, current_record=None):
        """Запрашивает и возвращает введенные поля записи."""
        last_name = input(
            f"Фамилия ({current_record.last_name}): ")\
            if current_record else input('Введите фамилию: ')
        first_name = input(
            f"Имя ({current_record.first_name}): ")\
            if current_record else input('Введите имя: ')
        middle_name = input(
            f"Отчество ({current_record.middle_name}): ")\
            if current_record else input(
                'Введите отчество: ')
        organization = input(
            f"Организация ({current_record.organization}): ")\
            if current_record else input(
                'Введите название организации: ')

        work_phone = self.validate_phone('Введите рабочий телефон: ')
        personal_phone = self.validate_phone('Введите личный телефон: ')

        return (last_name, first_name, middle_name,
                organization, work_phone, personal_phone)

    def has_records(self):
        """Проверяет наличие записей в телефонной книге и возвращает True,
         если есть записи."""
        if not self.records:
            print('Вы ещё не добавили контакты. \n')
            return False
        return True

    def add_records(self):
        """Функция добавления записей в телефонную книгу."""
        fields = self.input_record_fields()
        records = Records(*fields)
        self.records.append(records)
        self.save_data()
        print('Контакт добавлен. \n')

    def edit_records(self, records_idx: int):
        """Редактирование контактов в телефонной книге."""
        if 1 <= records_idx <= len(self.records):
            entry = self.records[records_idx - 1]
            print("Редактирование записи:")
            fields = self.input_record_fields(entry)
            (entry.last_name, entry.first_name,
             entry.middle_name, entry.organization,
             entry.work_phone, entry.personal_phone) = fields
            self.save_data()
            print("Запись обновлена.")
        else:
            print("Неверный индекс записи. \n")

    def show_records(self, page: int, per_page: int):
        """Вывод всех контактов по страницам."""
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        for index, record in enumerate(self.records[start_index:end_index],
                                       start=start_index + 1):
            self.result_print(index, record)

    def search_records(self):
        """Поиск контактов в телефонной книге."""
        search_field = input('Введите что хотите найти: ').lower()
        if search_field.strip():  # Проверка наличия хотя бы одного символа
            result = [record for record in self.records
                      if search_field in str(record).lower()]
            if result:
                print('Вот что удалось найти:')
                for index, record in enumerate(result, start=1):
                    self.result_print(index, record)
            else:
                print('Такой записи нет. \n')
        else:
            print('Поле поиска не может быть пустым.')


def main():
    """Основная функция."""
    phonebook = PhoneBook('phonebook.json')
    per_page = 5
    while True:
        print('Я твой телефонный справочник. Вот что я умею: ')
        print('1. Добавить контакт \n'
              '2. Показать мои контакты \n'
              '3. Редактировать контакт \n'
              '4. Поиск \n'
              '5. Выйти \n')
        choice = input('Введите номер команды: ')
        if choice == '1':
            phonebook.add_records()
        elif choice == '2':
            if not phonebook.has_records():
                continue
            page = int(input('Введите номер страницы: '))
            phonebook.show_records(page, per_page)
        elif choice == '3':
            if not phonebook.has_records():
                continue
            else:
                index = int(input('Введите номер записи для редактирования: '))
                phonebook.edit_records(index)
        elif choice == '4':
            if not phonebook.has_records():
                continue
            phonebook.search_records()
        elif choice == '5':
            print('Пока-пока, до встречи! \n'
                  'Хорошего дня!')
            break
        else:
            print('Вы ввели неверный номер команды \n'
                  'Попробуйте ещё раз.')


if __name__ == '__main__':
    main()
