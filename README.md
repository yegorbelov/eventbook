# EventBook – сервис бронирования билетов на мероприятия

Система бронирования билетов на мероприятия (театр, кино, выставки и т.д.)
на Python с веб-интерфейсом на Django.

## 1. Назначение

EventBook – учебное приложение для хранения информации о мероприятиях и
бронирования билетов. Консольная версия (ПР1–ПР3) дополнена веб-интерфейсом
на Django (ПР5), который в ПР6 переведён на систему шаблонов Django.

Целевая аудитория: люди, желающие разнообразить досуг посещением
мероприятий: дети с родителями, подростки, взрослые и пожилые люди.

## 2. Целевая аудитория

Люди, желающие разнообразить свой досуг посещением мероприятий:
дети с родителями, подростки, взрослые и пожилые люди.

## 3. Используемые технологии

- Python 3;
- Django 5.2;
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3;
- pytest, flake8, Git.

## 4. Предметная область

Основные сущности (классы в `models/`):

- `Event` – мероприятие: `id`, `name`, `date`, `venue`, `seats`, `price`;
  метод `has_capacity()` проверяет наличие свободных мест;
- `User` – пользователь: `id`, `name`;
- `Booking` – бронирование: `id`, `event`, `user`, `tickets_count`,
  `is_cancelled`; метод `cancel()` отменяет бронирование.

Бронирование хранит ссылки на объекты `Event` и `User`. Отменённое
бронирование не занимает места.

## 5. Веб-интерфейс

| URL                           | Страница              | View               |
| ----------------------------- | --------------------- | ------------------ |
| `/`                           | главная               | `index()`          |
| `/events/`                    | список мероприятий    | `events()`         |
| `/events/<int:event_id>/`     | страница мероприятия  | `event_detail()`   |
| `/bookings/`                  | список бронирований   | `bookings()`       |
| `/bookings/<int:booking_id>/` | страница бронирования | `booking_detail()` |

Если мероприятие или бронирование не найдено, страница возвращает код
статуса 404. Для несуществующих адресов настроен `handler404`.

## 6. Django Template Language

HTML формируется шаблонами, а не Python-кодом. Функция `page()` из ПР5
удалена. View-функции получают данные, формируют контекст и вызывают
`render()`.

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
  мероприятия.
- **Циклы и условия:** `{% for %}` с `{% empty %}` для пустых списков,
  `{% if %}` для статуса бронирования, наличия мест и случая
  «объект не найден».
- **Фильтры:** `{{ event.name|default:"Без названия" }}` – значение по умолчанию.
  Дата хранится строкой и выводится без преобразования.
- **Именованные URL и пространства имён:** `homepage:index`,
  `events:list`, `events:detail`, `bookings:bookings`, `bookings:detail`.
  Ссылки формируются тегом `{% url %}`.

## 7. Статические файлы

Расположены в `homepage/static/homepage/`:

- `css/style.css` – собственные стили проекта;
- `js/main.js` – вывод текущего года в подвале;
- `img/logo.png` – логотип и иконка вкладки.

Подключаются через `{% load static %}` и `{% static '...' %}`.

## 8. Структура проекта

```text
eventbook/
├── eventbook/
├── homepage/
├── events/
├── bookings/
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
├── tests/
├── main.py
├── storage.py
├── utils.py
├── manage.py
└── requirements.txt
```

## 9. Основные функции

`models/events.py`: `add_event`, `find_event`, `sort_events_by_date`,
`show_events`.
`models/users.py`: `add_user`, `find_user_by_name`, `find_or_create_user`.
`models/bookings.py`: `is_available`, `create_booking`, `cancel_booking`,
`find_booking_by_id`, `show_bookings`.
`storage.py`: `load_events`, `load_users`, `load_bookings` и
соответствующие `save_*`.

## 10. Запуск и проверка

```bash
pip install -r requirements.txt
python manage.py runserver
python manage.py check
pytest -v
flake8 . --extend-exclude=venv
```

## 11. План развития

- перенос сущностей в Django ORM и подключение базы данных;
- формы создания и отмены бронирований, добавления мероприятий;
- пользователи (регистрация, вход);
- API;
- контейнеризация и CI/CD.
