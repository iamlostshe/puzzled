"""Модуль для работы со страницей работы с клиентами."""

from __future__ import annotations

import datetime

import flet as ft
from loguru import logger

from pages.nav_bar import nav_bar
from utils import db


def edit_sells_page(page: ft.Page) -> ft.SafeArea:
    """Страница создания заказа."""
    data = {
        "status": "",
        "name": "",
        "num": "",
        "price": "",
        "sum": "",
        "client": "",
        "date_reg": "",
        "date_ready": "",
    }

    def choice_of_status_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Изменение статуса."""
        # Заносим изменения в data
        data["status"] = e.control.value

    def choice_of_puzzles_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Изменение товра."""
        # Заносим изменения в data
        data["name"] = e.control.value

    choice_of_status = ft.Dropdown(
        label="Статус",
        on_change=choice_of_status_on_click,
        options=[
            ft.dropdown.Option("Черновик"),
            ft.dropdown.Option("Согласовано с клиентом"),
            ft.dropdown.Option("На производстве"),
            ft.dropdown.Option("Готов к отгрузке"),
            ft.dropdown.Option("Отгружен клиенту"),
        ],
    )

    def get_options() -> list:
        """Получаем список всех пазлов."""
        # Инициализируем пустую переменную для результата
        result = []

        # Проходимся по всем пазлам
        p = db.Puzzles()
        for i in p.get():
            # Переводим пазл в удобный формат
            result.append(ft.dropdown.Option(i["name"]))

        # Возвращаем список всех пазлов
        return result

    # Получаем список всех пазлов
    options = get_options()

    choice_of_puzzles = ft.Dropdown(
        label="Товар",
        on_change=choice_of_puzzles_on_click,
        options=options,
    )

    def date_reg_change(e: ft.core.control_event.ControlEvent) -> None:
        """Отслеживание изменения времени."""
        data["date_reg"] = e.control.value.strftime("%d-%m-%Y %H:%M:%S")

    def date_ready_change(e: ft.core.control_event.ControlEvent) -> None:
        """Отслеживание изменения времени."""
        data["date_ready"] = e.control.value.strftime("%d-%m-%Y %H:%M:%S")

    date_reg_button = ft.ElevatedButton(
        "Выберите дату регистрации заказа",
        icon=ft.Icons.CALENDAR_MONTH,
        expand=True,
        width=page.width,
        on_click=lambda e: page.open(  # noqa: ARG005
            ft.DatePicker(
                on_change=date_reg_change,
                first_date=datetime.datetime.now(datetime.UTC).astimezone(),
                last_date=datetime.datetime(3000, 1, 1),
            ),
        ),
    )

    date_ready_button = ft.ElevatedButton(
        "Выберите дату выполнения заказа",
        icon=ft.Icons.CALENDAR_MONTH,
        width=page.width,
        on_click=lambda e: page.open(  # noqa: ARG005
            ft.DatePicker(
                on_change=date_ready_change,
                first_date=datetime.datetime.now(datetime.UTC).astimezone(),
                last_date=datetime.datetime(3000, 1, 1),
            ),
        ),
    )

    def choice_of_client_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Запоминает выбор клиента."""
        data["client"] = e.control.value

    def get_clients() -> list:
        """Создает список клиентов из бд в удобном формате."""
        # Получаем клиентов
        c = db.Clients()
        clients = c.get()

        # Инициализируем пустой список
        result = []

        # Проходимся по всем клиентам
        for client_name in clients:
            result.append(ft.dropdown.Option(client_name))

        return result

    clients = ft.Dropdown(
        label="Выбор клиента",
        on_change=choice_of_client_on_click,
        options=get_clients(),
    )

    def button_on_click(e: ft.core.control_event.ControlEvent) -> None:  # noqa: ARG001
        """Нажатие на кнопку 'Продолжить'."""
        # Получаем количество непустых полей в data
        len_data = len([1 for i in data.values() if i != ""])
        logger.debug(data)

        # Проверяем целостность data
        if len_data >= 6:
            # Записываем data в бд
            s = db.Sells()
            s.add(data)

            # Очищаем страницу
            page.clean()

            # Добавляем навигационное меню
            page.add(nav_bar(page, 1))

            # Открываем страницу продаж
            page.add(sells_page(page))

        # В ином случае выводим предупреждение
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Нужно заполнить все поля"))
            page.snack_bar.open = True
            page.update()

    button = ft.CupertinoFilledButton(
        text="Продолжить",
        expand=True,
        width=page.width,
        on_click=button_on_click,
    )

    def change_number(e: ft.core.control_event.ControlEvent) -> None:
        """Меняет количество товаров в data."""
        num = e.control.value
        logger.debug(num)
        logger.debug(not num)
        logger.debug(not num.isdigit())

        if not num:
            e.control.error_text = "Это поле не должно быть пустым"
        elif not num.isdigit():
            e.control.error_text = "Ввод должен быть числом"
        else:
            data["num"] = int(num)

        page.update()

    choice_number = ft.TextField(
        label="Кол-во",
        on_blur=change_number,
        expand=True,
    )

    def back(page: ft.Page) -> None:
        """Кнопка 'Назад'."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 1))

        # Открываем страницу клиента
        page.add(sells_page(page))

    return ft.SafeArea(
        ft.Column(
            width=page.width,
            controls=[
                ft.CupertinoFilledButton(
                    "Назад",
                    width=page.width,
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    on_click=lambda e: back(page),  # noqa: ARG005
                ),
                choice_of_status,
                date_reg_button,
                clients,
                date_ready_button,
                choice_of_puzzles,
                choice_number,
                button,
            ],
        ),
    )


def sells_page(page: ft.Page) -> None:
    """Страница работы с заказами."""

    def sells_page_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Нажатие на кнопку '+'."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 1))

        # Добавляем страницу создания пазлов
        page.add(edit_sells_page(page))

    plus_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda e: sells_page_on_click(e, page),
    )

    def get_items() -> list:
        """Собирет все заказы во едино."""
        c = db.Sells()
        return c.get()

    def get_table() -> ft.Row | ft.DataTable:
        """Функция для создания таблицы."""
        # Получаем информацию из бд
        items = get_items()

        # Если в бд нет ни одного товара
        if len(items) == 0:
            return ft.Row(
                controls=[
                    ft.Text("У Вас пока нет ни одного заказа("),
                ],
            )
        # Инициализируем пустой список для названий колнок
        columns = []

        # Подписываем колонки
        for column_name in (
            "№",
            "Статус",
            "Название",
            "Кол-во",
            "Цена",
            "Сумма",
            "Клиент",
            "Дата регистрации",
            "Дата исполнения",
        ):
            columns.append(ft.DataColumn(ft.Text(column_name)))

        # Инициализируем пустой список для строк
        rows = []

        # Записываем строки
        for c, row in enumerate(items):
            # Инициализируем пустой список под клетки
            cells = [ft.DataCell(ft.Text(c + 1))]

            # Проходимся по всем клеткам строки
            for i in row:
                # Добавляем новую клетку
                cells.append(ft.DataCell(ft.Text(row[i])))

            # Добавляем строку
            rows.append(ft.DataRow(cells))

        return ft.DataTable(columns=columns, rows=rows)

    table = get_table()

    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(label="Поиск заказов", expand=True),
                        plus_button,
                    ],
                ),
                table,
            ],
        ),
    )
