# EventBook – сервис бронирования билетов на мероприятия

Система бронирования билетов на мероприятия (театр, кино, выставки и т.д.)
на Python с веб-интерфейсом на Django.

## 1. Назначение

EventBook – учебное приложение для хранения информации о мероприятиях и
бронирования билетов. Консольная версия (ПР1–ПР3) дополнена веб-интерфейсом
на Django (ПР5), который в ПР6 переведён на систему шаблонов Django, в ПР7
получил реляционную базу данных SQLite, а в ПР9 переведён на Django ORM.

## 2. Целевая аудитория

Люди, желающие разнообразить свой досуг посещением мероприятий:
дети с родителями, подростки, взрослые и пожилые люди.

## 3. Используемые технологии

- Python 3;
- Django 5.2;
- SQLite, доступ к данным через Django ORM;
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3;
- pytest, flake8, Git.

## 4. Предметная область

Основные сущности веб-приложения – модели Django:

- `Event` (`events/models.py`) – мероприятие: `name`, `date`
  (дата и время), `venue`, `seats`, `price`; методы `booked_seats()` и
  `has_capacity()` считают занятые места по активным бронированиям;
- `User` (`users/models.py`) – пользователь предметной области: `name`.
  Это не встроенная модель аутентификации Django;
- `Booking` (`bookings/models.py`) – бронирование: `event`, `user`,
  `tickets_count`, `is_cancelled`; метод `cancel()` отменяет бронирование.

Поле `id` создаётся Django автоматически.

### Связи между моделями

- одно мероприятие может иметь несколько бронирований;
- один пользователь может создавать несколько бронирований;
- каждое бронирование относится к одному мероприятию и одному пользователю.

Связи «многие к одному» заданы полями `ForeignKey` в модели `Booking`:
`event` и `user`, у обоих `on_delete=PROTECT` (мероприятие или пользователь
с бронированиями не удаляются) и `related_name="bookings"`. Обратный
доступ: `event.bookings.all()`, `user.bookings.all()`.

Отменённое бронирование не занимает места.

### Консольная версия

Классы в пакете `models/` (`event.py`, `user.py`, `booking.py`) и функции
в `models/events.py`, `users.py`, `bookings.py` сохранены для консольной
версии (`main.py`). Данные консольной версии хранятся в `data/*.json`.
Веб-приложение эти классы не использует.

## 5. Веб-интерфейс

| URL                           | Страница                | View                 |
| ----------------------------- | ----------------------- | -------------------- |
| `/`                           | главная                 | `index()`            |
| `/events/`                    | список мероприятий      | `events()`           |
| `/events/<int:event_id>/`     | страница мероприятия    | `event_detail()`     |
| `/events/available/`          | свободные места на дату | `available_events()` |
| `/bookings/`                  | список бронирований     | `bookings()`         |
| `/bookings/<int:booking_id>/` | страница бронирования   | `booking_detail()`   |
| `/bookings/statistics/`       | статистика бронирований | `statistics()`       |

Если мероприятие или бронирование не найдено, возвращается ответ 404
(`get_object_or_404`). Для несуществующих адресов настроен `handler404`.

### Параметры запроса

- `/events/?q=<текст>` – поиск мероприятий по названию;
- `/events/available/?date=YYYY-MM-DD` – мероприятия на дату, в которых
  остались свободные места;
- `/bookings/` принимает параметры:
  - `q` – поиск по названию мероприятия или имени пользователя;
  - `date` – дата проведения мероприятия (`YYYY-MM-DD`);
  - `event` и `user` – идентификаторы мероприятия и пользователя;
  - `sort` – порядок: `date` (по умолчанию), `event`, `user`, `tickets`;
  - `page` – номер страницы (по 5 бронирований на странице).

Фильтры, поиск и сортировка работают совместно и сохраняются при
переходе между страницами. Некорректная дата, неизвестное значение
`sort` и неверный номер страницы не приводят к ошибке.

## 6. Django Template Language

HTML формируется шаблонами. View-функции получают данные через ORM,
формируют контекст и вызывают `render()`.

- **Базовый шаблон** `templates/base.html` содержит общую структуру
  страницы: подключение стилей, шапку, подвал, скрипт и блоки
  `{% block title %}` и `{% block content %}`.
- **Наследование:** дочерние шаблоны используют `{% extends "base.html" %}`.
- **Включаемые шаблоны** (`{% include %}`):
  `includes/header.html` (шапка и навигация),
  `events/includes/event_card.html` (карточка мероприятия),
  `bookings/includes/booking_status.html` (статус бронирования).
- **Контекст:** например, `{"events": events_list}` для списка
  мероприятий, `{"event": event, "available": available}` для страницы
  мероприятия, `{"bookings": page_obj, "page_obj": page_obj}` для списка
  бронирований.
- **Циклы и условия:** `{% for %}` с `{% empty %}` для пустых списков,
  `{% if %}` для статуса бронирования, наличия мест и вывода ошибок.
- **Фильтры:** `{{ event.date|date:"d.m.Y H:i" }}` – формат даты и времени.
- **Пагинация:** ссылки формируются тегом `{% querystring page=... %}`,
  который сохраняет остальные GET-параметры.
- **Именованные URL и пространства имён:** `homepage:index`,
  `events:list`, `events:detail`, `events:available`, `bookings:bookings`,
  `bookings:detail`, `bookings:statistics`. Ссылки формируются тегом
  `{% url %}`.

## 7. База данных и Django ORM

### Django ORM (ПР9)

Слой доступа к данным переведён с модуля `sqlite3` на Django ORM:
структура базы описывается моделями (раздел 4), а изменения структуры
оформляются миграциями (`events/migrations/`, `users/migrations/`,
`bookings/migrations/`). Файлы миграций хранятся в репозитории.

Django работает с базой, указанной в `DATABASES` (`db.sqlite3` в корне
проекта). Исходная база ПР7 `data/eventbook.sqlite` не изменяется и
используется только как источник данных при переносе.

Использованные возможности ORM:

- получение: `all()`, `get_object_or_404()`;
- фильтрация: `filter()` по одному и нескольким условиям, по полям
  связанных моделей (`event__date__date`), `exclude()`;
- поиск: `icontains` по строковому полю, `Q` по нескольким полям;
- сортировка: `order_by()` по одному и нескольким полям, по полю связанной
  модели, с проверкой значения через словарь допустимых полей;
- связи: `select_related()`, обратный доступ через `related_name`;
- сокращённый набор полей: `values()` с `annotate()` и `F()`;
- агрегирование и группировка: `aggregate()`, `annotate()`, `Count()`,
  `Sum()`, `Coalesce()`, условные выражения `Q` внутри агрегатных функций;
- постраничный вывод: `Paginator`.

Правила предметной области сохранены: отменённые бронирования не
учитываются в статистике и не занимают места, мероприятия без
бронирований остаются в статистике со значением 0.

### Перенос данных из базы ПР7

Таблицы Django создаются миграциями, данные переносятся скриптом
`db/import_sqlite_to_orm.py`: сначала мероприятия и пользователи,
затем бронирования со ссылками на них, одной транзакцией, с сохранением
исходных идентификаторов. Перед записью скрипт проверяет ссылочную
целостность, повторный запуск безопасен (`update_or_create`).
Структуру исходной базы выводит `db/inspect_source_db.py`.

### Предыдущая реализация (ПР7)

Схема SQLite описана в `sql/schema.sql`, запросы собраны в
`sql/queries.sql`, подключение – в `db/database.py`, импорт из JSON –
в `db/import_json.py`. Файлы сохранены как предыдущая реализация
предметной области, представления Django их больше не используют.

Таблицы исходной базы:

- `events` — `id`, `name`, `date`, `venue`, `seats`, `price`;
- `users` — `id`, `name`;
- `bookings` — `id`, `event_id`, `user_id`, `tickets_count`,
  `is_cancelled`; внешние ключи `event_id → events(id)` и
  `user_id → users(id)`.

## 8. Статические файлы

Расположены в `homepage/static/homepage/`:

- `css/style.css` – собственные стили проекта;
- `js/main.js` – вывод текущего года в подвале;
- `img/logo.png` – логотип и иконка вкладки.

Подключаются через `{% load static %}` и `{% static '...' %}`.

## 9. Структура проекта

```text
eventbook/
├── eventbook/
├── homepage/
├── events/
│   ├── models.py
│   ├── views.py
│   └── migrations/
├── users/
│   ├── models.py
│   └── migrations/
├── bookings/
│   ├── models.py
│   ├── views.py
│   └── migrations/
├── templates/
│   ├── base.html
│   └── includes/
│       └── header.html
├── models/
│   ├── event.py
│   ├── user.py
│   ├── booking.py
│   ├── events.py
│   ├── users.py
│   └── bookings.py
├── data/
│   ├── events.json
│   ├── users.json
│   ├── bookings.json
│   └── eventbook.sqlite
├── db/
│   ├── __init__.py
│   ├── database.py
│   ├── import_json.py
│   ├── inspect_source_db.py
│   └── import_sqlite_to_orm.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── tests/
├── main.py
├── storage.py
├── utils.py
├── manage.py
└── requirements.txt
```

## 10. Основные функции

`models/events.py`: `add_event`, `find_event`, `sort_events_by_date`,
`show_events`.
`models/users.py`: `add_user`, `find_user_by_name`, `find_or_create_user`.
`models/bookings.py`: `is_available`, `create_booking`, `cancel_booking`,
`find_booking_by_id`, `show_bookings`.
`storage.py`: `load_events`, `load_users`, `load_bookings` и
соответствующие `save_*`.

`events/views.py`: `with_free_seats` (занятые и свободные места через
`annotate`), `events`, `event_detail`, `available_events`.
`bookings/views.py`: `bookings` (поиск, фильтры, сортировка, пагинация),
`booking_detail`, `statistics`.

## 11. Запуск и проверка

```bash
pip install -r requirements.txt
python manage.py migrate
python db/import_sqlite_to_orm.py
python manage.py runserver
```

Команда `import_sqlite_to_orm.py` переносит данные из `data/eventbook.sqlite`
в базу Django и выводит количество записей в источнике и в целевой базе.
Файл `db.sqlite3` не хранится в репозитории: после клонирования таблицы
создаются миграциями, а данные переносятся скриптом.

Проверки:

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=venv
```

## 12. План развития

- формы создания и отмены бронирований, добавления мероприятий;
- пользователи (регистрация, вход);
- API;
- контейнеризация и CI/CD.
