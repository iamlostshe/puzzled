'Модуль для работы с главной страницей'

import flet as ft

from pages.nav_bar import nav_bar

from utils import db


def edit_main_page(page: ft.Page) -> None:
    'Страница добавления новых пазлов'

    def eng(word: str) -> str:
        'Систематизирует data'

        return {
            'Название пазла': 'name',
            'Толщина, мм': 'width',
            'Кол-во деталей, шт.': 'num_details'
        }[word]


    def is_rectangle_possible(n: int | str):
        'Проверка возможен ли пазл из заданного количества деталей'

        # Переводим n в числовой формат
        n = int(n)

        # Невозможно собрать пазл из 0 или отрицательного количества элементов
        if n <= 0:
            return False
        for width in range(2, int(n**0.5) + 1):
            if n % width == 0:
                height = n // width
                if width > 0 and height > 0:
                    return True
        return False


    def check_form(e):
        'Функция для проверки формы'

        e.control.error_text = None
        text = e.control.value

        # Проверяем запонена ли форма
        if not text and e.control.label != 'Название пазла':
            e.control.error_text = 'Это поле не должно быть пустым'
        
        # Проверяем заполнена ли она числом
        elif e.control.label in ["Толщина, мм", 'Кол-во деталей, шт.'] and not text.isdigit():
            e.control.error_text = 'Ввод должен быть числом'

        # Проверяем есть ли ввод среди доступных размеров
        elif e.control.label == "Толщина, мм" and not int(text) in [3, 4, 6, 9]:
            e.control.error_text = 'Ввод должен быть одним среди 3 4 6 9'

        # Проверяем возможен ли пазл с таким количеством деталей
        elif e.control.label == "Кол-во деталей, шт." and not is_rectangle_possible(text):
            e.control.error_text = 'Пазл из такого количества деталей невозможен'

        # В ином случае
        else:
            # Запишем данные в словарь
            data[eng(e.control.label)] = e.control.value

        # Обновляем страницу
        e.control.update()
        

    def submit_form(e, page: ft.Page) -> None:
        'Сохраняет результат формы'

        # Получаем непустые строки
        len_data = 0

        for i in data:
            print(data[i])
            if data[i] != '' or i in ['name', 'time', 'price']:
                len_data += 1

        # Если информации достаточно
        if len_data >= 6:
            # Если нужно заполняем name
            if data['name'] == '':
                data['name'] = f'{data['tree_type']}-{data['width']}'

            # Записываем её в JSON бд
            p = db.Puzzles()
            p.add(data)

            # Очищаем страницу
            page.clean()

            # Переходим на главную
            page.add(main_page(page))

            # Добавляем навигационное меню
            page.add(nav_bar(page, 0))

        # В ином случае выводим предупреждение
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Нужно заполнить все поля'))
            page.snack_bar.open = True
            page.update()


    def choice_of_tree_on_click(e):
        'Выбор вида древисины'

        # Запишем изменения в data
        data['tree_type'] = e.control.value

    # Выпадающий список выбора древисины
    choice_of_tree = ft.Dropdown(
        label="Вид древесины",
        on_change=choice_of_tree_on_click,
        options=[
            ft.dropdown.Option('Береза'),
            ft.dropdown.Option('Сосна'),
            ft.dropdown.Option('Клен'),
            ft.dropdown.Option('Махагон'),
            ft.dropdown.Option('Дуб'),
            ft.dropdown.Option('Тик'),
            ft.dropdown.Option('Липа'),
            ft.dropdown.Option('Вишня')
        ]
    )

    # Инициализируем словарь с пустыми значениями
    data = {
        'time': '',
        'name': '',
        'price': '',
        'tree_type': '',
        'width': '',
        'num_details': ''
    }

    # Кнопка подтверждения отправки данных
    submit = ft.CupertinoFilledButton("Продолжить", on_click=lambda e: submit_form(e, page))

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            controls=[
                ft.Text(
                    value='Фанерный лист'
                ),
                ft.TextField(
                    label='Название пазла',
                    keyboard_type=ft.KeyboardType.TEXT,
                    on_blur=check_form
                ),
                choice_of_tree,
                ft.TextField(
                    label='Толщина, мм',
                    keyboard_type=ft.KeyboardType.NUMBER,
                    on_blur=check_form
                ),
                ft.TextField(
                    label='Кол-во деталей, шт.',
                    keyboard_type=ft.KeyboardType.NUMBER,
                    on_blur=check_form
                ),
                ft.Row(controls=[submit], alignment=ft.MainAxisAlignment.CENTER)
            ]
        )
    )


def main_page(page: ft.Page) -> ft.SafeArea:
    'Главное меню'

    def main_page_on_click(e, page: ft.Page) -> None:
        'Нажатие на кнопку "+"'

        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 0))

        # Добавляем страницу создания пазлов
        page.add(edit_main_page(page))

    
    def get_items() -> list:
        'Получаем данные из бд'

        p = db.Puzzles()
        return p.get()


    def get_table(items: list) -> ft.Row | ft.DataTable:
        'Функция для создания таблицы'

        # Если в бд нет ни одного товара
        if len(items) == 0:
            return ft.Row(
                controls=[
                    ft.Text('У Вас пока нет ни одного шаблона пазла('),
                ]
            )
        else:
            # Инициализируем пустой список для названий колнок
            columns = []

            # Подписываем колонки
            for column_name in (
                '№', 'Дата', 'Имя', 'Цена', 'Вид древесины', 'Толщина', 'Кол-во деталей, шт.'
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

        # Возвращаем таблицу
        return ft.DataTable(
            width=page.width,
            columns=columns,
            rows=rows
        )

    # Кнопка добавления нового пазла
    plus_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: main_page_on_click(e, page))

    # Получаем информацию из бд
    items = get_items()
    table = get_table(items)

    def search_puzzles(e, page: ft.Page) -> None:
        'Поиск пазлов'

        # Поиск по бд
        db.Puzzles.search(e.control.value)

        # Обновлённая таблица
        table = get_table(items)

        # Обновляем страницу
        page.update()

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label='Поиск пазлов',
                            expand=True,
                            on_blur=lambda e: search_puzzles(e, page)),
                        plus_button
                    ]
                ),
                table
            ]
        )
    )
