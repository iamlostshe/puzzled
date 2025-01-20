# Пояснительная записка

### Как запустить?

1. Windows

Открыть эту папку в коммандной строке и ввести:

```
start dist\main.exe
```

Или вручную открыть файл `dist\main.exe`.

2. Linux

Открыть эту папку в коммандной строке и ввести:

```
dist\main
```

3. Mac OS

Открыть эту папку в коммандной строке и ввести:

```
open dist\main.app
```

# Небольшое описание

- Проект написан на python-фреймворке `flet`.

- Все соответствует стандарту `PEP-8`.

- Цена пазла считается по формуле:

```
(цена выбранного вида древисины + толщина, мм + кол-во деталей) * index (задаётся в db/price_list.json)
```

В случае если менеджер захочет изменить цену на всю продукцию, то он просто поменяет `index` в файле `db/price_list.json` в соответствую сторону.

Если поставщик какого-либо вида древесины изменит цену - менеджер также сможет изменить ее в файле `db/price_list.json`.

- Экспорт осуществляется в папку `/export` (можно изменить в config.py).

### Структура проекта

```
db        - все файлы баз данных
images    - изображения для тз
pages     - страницы flet для приложения
res       - ресурсы (шрифт)
utils     - утилиты (работа с бд)
config.py - файл конфига 
main.py   - файл запуска приложения
README.md - пояснительная записка

pyproject.toml - конфигурация линтера (`ruff` и `poetry`)

tz.md и pre-tz.md - тех. задание
```

### Как развернуть

1. Клонируем репозиторий:

``` bash
git clone https://github.com/iamlostshe/puzzled
```

2. Устанавливаем зависимости через `poetry`:

<details>
<summary>
Установка poetry (если не установлен)
</summary>

Linux:

``` bash
curl -sSL https://install.python-poetry.org | python3 -
```

Windows:

``` bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

</details>

``` bash
poetry install
```

<details>
<summary>
Или через `requirements.txt`
</summary>

``` bash
pip3 install -r requirements.txt
```

</details>

3. Запускаем проект:

```
python3 main.py
```
