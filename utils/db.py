'Модуль для работы с JSON базой данных'

import json
from datetime import datetime
import os

from loguru import logger

from config import (
    REPORT_SEP,
    REPORT_NAME_TXT, REPORT_NAME_JSON,
    REPORT_DIR, REPORT_DB_NAME,
    PUZZLES_DB_NAME, CLIENTS_DB_NAME,
    SELLS_DB_NAME, PRICE_LIST_DB_NAME
)

def get_time() -> str:
    'Получаем время в правильном формате'

    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")


def check_db():
    'Проверяет наличае файла бд в папке и создает его при необходимости'

    # Проверка наличая всех необходимых папок
    for dir_name in [
        REPORT_DIR
    ]:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    # Проверка наличая всех необходимых файлов
    for filename in [
        REPORT_DB_NAME, PUZZLES_DB_NAME,
        CLIENTS_DB_NAME, SELLS_DB_NAME,
        PRICE_LIST_DB_NAME
    ]:
        if not os.path.exists(filename):
            with open(filename, 'a', encoding='UTF-8') as f:
                f.write('[]\n')
    

class Puzzles:
    'Класс для работы с бд пазлов'

    def get_price(self, tree_type: str, width: str | int, num_details: str | int):
        'Получаем цену пазла'

        # Открываем прайс-лист для получения цен
        with open(PRICE_LIST_DB_NAME, 'r', encoding='UTF-8') as f:
            # Десериализуем JSON
            data = json.load(f)

        # Считаем и возвращаем цену пазла
        return (
            data['tree'][tree_type] + int(width) + int(num_details)
        ) * data['index']


    def add(self, my_data: dict):
        'Добавляет пользователя в JSON базу данных'

        with open(PUZZLES_DB_NAME, 'r+', encoding='UTF-8') as f:
            data = json.load(f)

            my_data['time'] = get_time()
            my_data['price'] = self.get_price(
                tree_type=my_data['tree_type'],
                width=my_data['width'],
                num_details=my_data['num_details']
            )

            data.append(my_data)

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)

            logger.debug('Новый пазл! {}', my_data)


    def get(self) -> list:
        'Возвращает все объекты JSON базы данных'

        with open(PUZZLES_DB_NAME, 'r', encoding='UTF-8') as f:
            data = json.load(f)

        return data


class Clients:
    'Класс для взаимодействия с бд клиентов'

    def get(self) -> list:
        'Возвращает список всех клиентов'

        # Открываем бд клиентов
        with open(CLIENTS_DB_NAME, 'r', encoding='UTF-8') as f:
            # Дисериализуем JSON
            return json.load(f)


class Sells:
    'Класс для взаимодействия с бд клиентов'

    def add(self, my_data: dict) -> None:
        'Добавляет нового клиента'

        with open(SELLS_DB_NAME, 'r+', encoding='UTF-8') as f:
            data = json.load(f)

            my_data['time'] = get_time()

            data.append(my_data)

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)

            logger.debug('Новый клиент! {}', my_data)


    def get(self) -> list:
        'Возвращает список всех клиентов'

        # Открываем бд клиентов
        with open(SELLS_DB_NAME, 'r', encoding='UTF-8') as f:
            # Дисериализуем JSON
            return json.load(f)


class Reports:
    'Класс для взаимодействия с бд отчётов'

    def json_to_txt(self, data: list):
        'Перевод json в txt'

        # Инициализируем пустой список
        result = []

        for a, b in enumerate(data):
            if isinstance(b, dict):

                # Инициализируем пустой список
                pre_result = []

                # Проходимся по словарю
                for c in b:
                    pre_result.append(f'{c} - {data[a][c]}')
            
                # Добавляем результат в список
                result.append('\n'.join(pre_result))

        return '\n\n---\n\n'.join(result)

    def add(self, r_type: str, r_format: str) -> None:
        'Создание нового отчёта'

        # Выбираем файл для отчёта
        r_filename = {
            'Прайс-лист': PRICE_LIST_DB_NAME,
            'Продажи': SELLS_DB_NAME,
            'Пазлы': PUZZLES_DB_NAME,
            'Клиенты': CLIENTS_DB_NAME
        }[r_type]

        # Открываем JSON
        with open(r_filename, 'r', encoding='UTF-8') as f:
            text = f.read()

        # Переводим JSON в TXT если это необходимо
        if r_format == 'txt':
            text = self.json_to_txt(text)

        # Переводим r_format в нижний регистр
        r_format = r_format.lower()

        # Имя будующего файла
        filename = {
            'txt': f'{REPORT_NAME_TXT}.txt',
            'json': f'{REPORT_NAME_JSON}.json'
        }[r_format]

        # Готовим дату и время
        now_time = get_time()

        for sep in ':- ':
            now_time = now_time.replace(sep, REPORT_SEP)

        # Подставляем дату и время
        filename = filename.replace('<data-time>', now_time)

        # Записываем файл
        with open(f'{REPORT_DIR}/{filename}', 'a', encoding='UTF-8') as f:
            f.write(text)

        # Заносим информацию ою отчёте в базу
        with open(REPORT_DB_NAME, 'r+', encoding='UTF-8') as f:
            data = json.load(f)

            data.append(
                {
                    'r_type': r_type,
                    'r_format': r_format,
                    'time': get_time()
                }
            )

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)


    def get(self) -> list:
        'Возвращает список из всех отчётов'

        # Открываем JSON бд для чтения
        with open(REPORT_DB_NAME, 'r', encoding='UTF-8') as f:
            data = json.load(f)

        return data
