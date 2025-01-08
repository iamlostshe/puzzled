'Модуль для работы с навигационным меню'

import flet as ft


def nav_bar(page: ft.Page, index: int | None = None) -> ft.NavigationBar:
    'Создаёт навигационное меню'

    if not index:
        index = 0

    return ft.NavigationBar(
        on_change=lambda e: nav_bar_on_change(e, page),
        selected_index=index,
        destinations=[
            ft.NavigationBarDestination(
                label='Главная',
                icon=ft.Icons.HOME_ROUNDED,
                selected_icon=ft.Icons.HOME_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label='Заказы',
                icon=ft.Icons.PEOPLE,
                selected_icon=ft.Icons.PEOPLE_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label='Склад',
                icon=ft.Icons.WAREHOUSE,
                selected_icon=ft.Icons.WAREHOUSE_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label='Отчеты',
                icon=ft.Icons.DOCUMENT_SCANNER_ROUNDED,
                selected_icon=ft.Icons.DOCUMENT_SCANNER_OUTLINED,
            ),
        ]
    )


def nav_bar_on_change(e, page: ft.Page):
    'Запускается при изменении навигационного меню'

    from pages.main import main_page
    from pages.sells import clients_page
    from pages.warehouse import warehouse_page
    from pages.reports import reports_page


    # Определяем какая страница выбрана
    num = int(e.data)

    # Очищаем страницу
    page.clean()

    # Добавляем навигационное меню
    page.add(nav_bar(page, num))

    # Главная
    if num == 0:
        page.add(main_page(page))

    # Работа с клиентами
    elif num == 1:
        page.add(clients_page(page))

    # Склад
    elif num == 2:
        page.add(warehouse_page(page))

    # Отчёты
    elif num == 3:
        page.add(reports_page(page))
