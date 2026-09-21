from datetime import datetime

event_name = "Спектакль «Ревизор»"
event_datetime = datetime(2026, 10, 15, 19, 0)
total_seats = 50
price_per_ticket = 800
age_limit = 12

user_name = "Иван Петров"
user_age = 25
tickets_requested = 2
is_booked = True


def is_seats_available(total_seats: int, tickets_requested: int) -> bool:
    return total_seats >= tickets_requested


def get_booking_status(is_booked: bool) -> str:
    if is_booked:
        return "Бронирование подтверждено"
    return "Бронирование отменено"


def calculate_total_price(price_per_ticket: float, tickets_requested: int) -> float:
    return price_per_ticket * tickets_requested


def check_age_restriction(user_age: int, age_limit: int) -> bool:
    return user_age >= age_limit


print(f"Мероприятие: {event_name}")
print(f"Дата и время: {event_datetime.strftime('%d.%m.%Y %H:%M')}")
print(f"Цена билета: {price_per_ticket} руб.")
print(f"Возрастное ограничение: {age_limit}+")
print()

print(f"Пользователь: {user_name}, возраст: {user_age}")

if not check_age_restriction(user_age, age_limit):
    print("Бронирование невозможно: возрастное ограничение не пройдено")
elif not is_seats_available(total_seats, tickets_requested):
    print("Бронирование невозможно: нет свободных мест")
else:
    total_price = calculate_total_price(price_per_ticket, tickets_requested)
    print(f"Количество билетов: {tickets_requested}")
    print(f"Итоговая стоимость: {total_price} руб.")
    print(get_booking_status(is_booked))