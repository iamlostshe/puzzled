"""Модуль для работы с отчётами."""

from __future__ import annotations

import flet as ft

from pages.nav_bar import nav_bar
from utils import db


def edit_reports_page(page: ft.Page) -> ft.SafeArea:
    """Меню создания отчёта."""

    def save_file(name: str) -> None:
        """Функция для сохранения отчётов."""
        r = db.Reports()
        filename = r.add(name)

        file_piker = ft.FilePicker()
        file_piker.save_file(
            dialog_title=f"Куда сохранить {filename}?",
            file_name=filename,
            file_type=ft.FilePickerFileType.CUSTOM,
        )

    def choice_of_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Обработка выбора вида отчёта."""
        # Присваиваем правильное имя
        name = {"Вид отчёта": "type", "Формат отчёта": "format"}[e.control.label]

        # Заносим вид отчёта в data
        data[name] = e.control.value

    def button_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Сохраняет ввод и переводит на страницу отчётов."""
        # Считаем количество заполненых полей
        len_data = 0

        len_data = len([1 for i in data.items() if i != ""])

        if len_data >= 2:
            # Записываем её в JSON бд
            r = db.Reports()
            r.add(data["type"], data["format"])

            # Очищаем страницу
            page.clean()

            # Переходим на страницу отчётов
            page.add(reports_page(page))

            # Добавляем навигационное меню
            page.add(nav_bar(page, 3))

        # В ином случае выводим предупреждение
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Нужно заполнить все поля"))
            page.snack_bar.open = True
            page.update()

    data = {"type": "", "format": ""}

    choice_of_report = ft.Dropdown(
        label="Вид отчёта",
        on_change=choice_of_on_click,
        options=[
            ft.dropdown.Option("Прайс-лист"),
            ft.dropdown.Option("Продажи"),
            ft.dropdown.Option("Пазлы"),
            ft.dropdown.Option("Клиенты"),
        ],
    )

    choice_of_format = ft.Dropdown(
        label="Формат отчёта",
        on_change=choice_of_on_click,
        options=[ft.dropdown.Option("JSON"), ft.dropdown.Option("TXT")],
    )

    button = ft.CupertinoFilledButton(
        text="Продолжить",
        width=page.width,
        on_click=lambda e: button_on_click(e, page),
    )

    def back(page: ft.Page) -> None:
        """Кнопка 'Назад'."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 3))

        # Открываем страницу клиента
        page.add(reports_page(page))

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
                choice_of_report,
                choice_of_format,
                button,
            ],
        ),
    )


def reports_page(page: ft.Page) -> ft.SafeArea:
    """Страница работы с отчётами."""

    def reports_page_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Нажатие на кнопку '+'."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 3))

        # Добавляем страницу создания пазлов
        page.add(edit_reports_page(page))

    def get_items() -> list:
        """Собирет все отчёты во едино."""
        p = db.Reports()
        return p.get()

    def get_table() -> ft.Row | ft.DataTable:
        """Функция для создания таблицы."""
        # Получаем информацию из бд
        items = get_items()

        # Если в бд нет ни одного товара
        if len(items) == 0:
            return ft.Row(
                controls=[
                    ft.Text("У Вас пока нет ни одного отчёта("),
                ],
            )
        # Инициализируем пустой список для названий колнок
        columns = []

        # Подписываем колонки
        for column_name in ("№", "Вид отчёта", "Формат отчёта", "Дата и время"):
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

        return ft.DataTable(width=page.width, columns=columns, rows=rows)

    plus_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda e: reports_page_on_click(e, page),
    )

    table = get_table()

    return ft.SafeArea(
        ft.Column(
            width=page.width,
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(label="Поиск отчётов", expand=True),
                        plus_button,
                    ],
                ),
                table,
            ],
        ),
    )
