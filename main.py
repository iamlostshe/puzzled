"""Модуль для запуска приложения."""

import flet as ft
from loguru import logger

from config import FONT_PATH
from pages.main import main_page
from pages.nav_bar import nav_bar
from utils import db


def main(page: ft.Page) -> None:
    """Функция для запуска приложения."""
    # Проверяем наличае JSON базы данных
    db.check_db()

    # Подключаем файл для логов
    logger.add("log.log")

    # Подключаем шрифт из файла
    page.fonts = {
        "Hack": FONT_PATH,
    }
    page.theme = ft.Theme(font_family="Hack")

    # Задаём название приложению
    page.title = "Puzzled"

    # Добавляем навигационное меню
    page.add(nav_bar(page))

    # Открываем стартовую страницу
    page.add(main_page(page))


if __name__ == "__main__":
    ft.app(target=main)
