'Модуль для работы с страницей склада'

import flet as ft


# TODO def edit_warehouse_page(page: ft.Page) -> ft.SafeArea:
    # return ft.SafeArea(
        # )

def warehouse_page(page: ft.Page) -> ft.SafeArea:
    'Страница работы со складом'

    def warehouse_page_on_click(e, page: ft.Page) -> None:
        'Нажатие на кнопку "+"'

        page.snack_bar = ft.SnackBar(ft.Text('Этот раздел пока в разработке...'))
        page.snack_bar.open = True
        page.update()

    plus_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: warehouse_page_on_click(e, page))

    return ft.SafeArea(
        ft.Column(
            width=page.width,
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(label='Поиск отчётов', expand=True),
                        plus_button
                    ]
                )
                # TODO table
            ]
        )
    )
