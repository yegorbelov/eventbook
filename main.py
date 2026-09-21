from events import add_event, find_event, show_events, sort_events_by_date
from bookings import cancel_booking, create_booking, show_bookings
from storage import load_data, save_data
from utils import input_int

EVENTS_FILE = "data/events.json"
BOOKINGS_FILE = "data/bookings.json"

MENU = """
=== Бронирование билетов на мероприятия ===
1. Показать мероприятия (по дате)
2. Добавить мероприятие
3. Забронировать билеты
4. Отменить бронирование
5. Показать бронирования
0. Выход
"""


def main():
    events = load_data(EVENTS_FILE)
    bookings = load_data(BOOKINGS_FILE)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_events(sort_events_by_date(events))

        elif choice == "2":
            name = input("Название: ")
            date = input("Дата (ГГГГ-ММ-ДД): ")
            venue = input("Место проведения: ")
            seats = input_int("Количество мест: ")
            price = input_int("Цена билета: ")
            add_event(events, name, date, venue, seats, price)
            print("Мероприятие добавлено.")

        elif choice == "3":
            show_events(events)
            event_id = input_int("ID мероприятия: ")
            event = find_event(events, event_id)
            if event is None:
                print("Мероприятие не найдено.")
                continue
            user_name = input("Ваше имя: ")
            tickets_count = input_int("Количество билетов: ")
            booking = create_booking(bookings, event, user_name, tickets_count)
            if booking is None:
                print("Недостаточно свободных мест.")
            else:
                print(f"Бронирование создано, ID: {booking['id']}.")

        elif choice == "4":
            booking_id = input_int("ID бронирования: ")
            if cancel_booking(bookings, booking_id):
                print("Бронирование отменено.")
            else:
                print("Бронирование не найдено.")

        elif choice == "5":
            show_bookings(bookings)

        elif choice == "0":
            save_data(EVENTS_FILE, events)
            save_data(BOOKINGS_FILE, bookings)
            print("До свидания!")
            break

        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    main()
