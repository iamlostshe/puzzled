"""Модуль для работы с навигационным меню."""

from __future__ import annotations

import flet as ft

# Главная
MAIN_PAGE_INDEX = 0

# Заказы
SELLS_PAGE_INDEX = 1

# Склад
WAREHOUSE_PAGE_INDEX = 2

# Отчёты
REPORTS_PAGE_INDEX = 3


def nav_bar(page: ft.Page, index: int | None = None) -> ft.NavigationBar:
    """Создаёт навигационное меню."""
    if not index:
        index = 0

    return ft.NavigationBar(
        on_change=lambda e: nav_bar_on_change(e, page),
        selected_index=index,
        destinations=[
            ft.NavigationBarDestination(
                label="Главная",
                icon=ft.Icons.HOME_ROUNDED,
                selected_icon=ft.Icons.HOME_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Заказы",
                icon=ft.Icons.PEOPLE,
                selected_icon=ft.Icons.PEOPLE_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Склад",
                icon=ft.Icons.WAREHOUSE,
                selected_icon=ft.Icons.WAREHOUSE_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Отчеты",
                icon=ft.Icons.DOCUMENT_SCANNER_ROUNDED,
                selected_icon=ft.Icons.DOCUMENT_SCANNER_OUTLINED,
            ),
        ],
    )


def nav_bar_on_change(e: ft.core.control_event.ControlEvent, page: ft.Page) -> None:
    """Запускается при изменении навигационного меню."""
    from pages.main import main_page
    from pages.reports import reports_page
    from pages.sells import sells_page
    from pages.warehouse import warehouse_page

    # Определяем какая страница выбрана
    num = int(e.data)

    # Очищаем страницу
    page.clean()

    # Добавляем навигационное меню
    page.add(nav_bar(page, num))

    # Главная
    if num == MAIN_PAGE_INDEX:
        page.add(main_page(page))

    # Заказы
    elif num == SELLS_PAGE_INDEX:
        page.add(sells_page(page))

    # Склад
    elif num == WAREHOUSE_PAGE_INDEX:
        page.add(warehouse_page(page))

    # Отчёты
    elif num == REPORTS_PAGE_INDEX:
        page.add(reports_page(page))
