"""Модуль для работы с JSON базой данных."""

from __future__ import annotations

import datetime
import json
from pathlib import Path

from loguru import logger

from config import (
    CLIENTS_DB_NAME,
    PRICE_LIST_DB_NAME,
    PUZZLES_DB_NAME,
    REPORT_DB_NAME,
    REPORT_DIR,
    REPORT_NAME_JSON,
    # REPORT_NAME_PNG,
    REPORT_NAME_TXT,
    REPORT_SEP,
    SELLS_DB_NAME,
)


def search(filename: str, search_key: str) -> list:
    """Поиск по базе данных."""
    with Path.open(filename, encoding="UTF-8") as f:
        data = json.load(f)

    logger.debug(data)

    result = [i for i in data if search_key.lower() in " ".join(i).lower()]
    logger.debug(result)

    if not result:
        result.append("По вашему запросу ничего не найдено(")

    return result


def get_time() -> str:
    """Получаем время в правильном формате."""
    now = datetime.datetime.now(datetime.UTC).astimezone()
    return now.strftime("%d-%m-%Y %H:%M:%S")


def check_db() -> None:
    """Проверяет наличае файла бд в папке и создает его при необходимости."""
    # Проверка наличая всех необходимых папок
    for dir_name in [REPORT_DIR]:
        path = Path(dir_name)

        if not path.exists():
            Path.mkdir(dir_name)
            logger.debug('Directory "{}" was successfully created.', dir_name)

    # Проверка наличая всех необходимых файлов
    for filename in [
        REPORT_DB_NAME,
        PUZZLES_DB_NAME,
        CLIENTS_DB_NAME,
        SELLS_DB_NAME,
        PRICE_LIST_DB_NAME,
    ]:
        path = Path(filename)

        if not path.exists():
            with Path.open(filename, "a", encoding="UTF-8") as f:
                f.write("[]\n")
            logger.debug('File "{}" was successfully created.', filename)


class Puzzles:
    """Класс для работы с бд пазлов."""

    def search(self, search_key: str) -> str:
        """TODO: Недоделаный поиск."""
        logger.debug(search(PUZZLES_DB_NAME, search_key))
        return search(PUZZLES_DB_NAME, search_key)

    def get_price(
        self,
        tree_type: str,
        width: str | int,
    ) -> float:
        """Получаем цену пазла."""
        # Открываем прайс-лист для получения цен
        with Path.open(PRICE_LIST_DB_NAME, "r", encoding="UTF-8") as f:
            # Десериализуем JSON
            data = json.load(f)

        # Считаем и возвращаем цену пазла

        # `цена 1 мм выбранного вида древисины (задаётся в db/price_list.json)` *
        # `толщина, мм` * `index (задаётся в db/price_list.json)`
        return data["tree"][tree_type] * int(width) * data["index"]

    def add(self, my_data: dict) -> None:
        """Добавляет пользователя в JSON базу данных."""
        with Path.open(PUZZLES_DB_NAME, "r+", encoding="UTF-8") as f:
            data = json.load(f)

            my_data["time"] = get_time()
            my_data["price"] = self.get_price(
                tree_type=my_data["tree_type"],
                width=my_data["width"],
            )

            data.append(my_data)

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)

            logger.debug("Новый пазл! {}", my_data)

    def get(self) -> list:
        """Возвращает все объекты JSON базы данных."""
        with Path.open(PUZZLES_DB_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)


class Clients:
    """Класс для взаимодействия с бд клиентов."""

    def get(self) -> list:
        """Возвращает список всех клиентов."""
        # Открываем бд клиентов
        with Path.open(CLIENTS_DB_NAME, "r", encoding="UTF-8") as f:
            # Дисериализуем JSON
            return json.load(f)


class Sells:
    """Класс для взаимодействия с бд клиентов."""

    def add(self, my_data: dict) -> None:
        """Добавляет нового клиента."""
        with Path.open(SELLS_DB_NAME, "r+", encoding="UTF-8") as f:
            data = json.load(f)

            my_data["time"] = get_time()

            data.append(my_data)

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)

            logger.debug("Новый клиент! {}", my_data)

    def get(self) -> list:
        """Возвращает список всех клиентов."""
        # Открываем бд клиентов
        with Path.open(SELLS_DB_NAME, "r", encoding="UTF-8") as f:
            # Дисериализуем JSON
            return json.load(f)


class Reports:
    """Класс для взаимодействия с бд отчётов."""

    def add(self, r_type: str, r_format: str) -> None:
        """Создание нового отчёта."""
        # Выбираем файл для отчёта
        r_filename = {
            "Прайс-лист": PRICE_LIST_DB_NAME,
            "Продажи": SELLS_DB_NAME,
            "Пазлы": PUZZLES_DB_NAME,
            "Клиенты": CLIENTS_DB_NAME,
        }[r_type]

        # Открываем JSON
        with Path.open(r_filename, "r", encoding="UTF-8") as f:
            text = f.read()

        # Переводим r_format в нижний регистр
        r_format = r_format.lower()

        # TODO: Переводим JSON в TXT если это необходимо
        # if r_format == "txt":
        #     text = self.json_to_txt(text)
        #     logger.debug(text)

        # Имя будующего файла
        filename = {
            # "график": f"{REPORT_NAME_PNG}.png",
            "txt": f"{REPORT_NAME_TXT}.txt",
            "json": f"{REPORT_NAME_JSON}.json",
        }[r_format]

        # Готовим дату и время
        now_time = get_time()

        for sep in ":- ":
            now_time = now_time.replace(sep, REPORT_SEP)

        # Подставляем дату и время
        filename = filename.replace("<data-time>", now_time)

        # Записываем файл
        with Path.open(f"{REPORT_DIR}/{filename}", "a", encoding="UTF-8") as f:
            f.write(text)

        # Заносим информацию ою отчёте в базу
        with Path.open(REPORT_DB_NAME, "r+", encoding="UTF-8") as f:
            data = json.load(f)

            data.append(
                {
                    "r_type": r_type,
                    "r_format": r_format,
                    "filename": f"{REPORT_DIR}/{filename}",
                    "time": get_time(),
                },
            )

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get(self) -> list:
        """Возвращает список из всех отчётов."""
        # Открываем JSON бд для чтения
        with Path.open(REPORT_DB_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)
