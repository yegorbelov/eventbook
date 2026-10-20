-- 1. Список мероприятий по дате
SELECT id, name, date, venue, seats, price
FROM events
ORDER BY date;

-- 2. Список пользователей
SELECT id, name
FROM users
ORDER BY name;

-- 3. WHERE: мероприятия с числом мест не меньше 100
SELECT id, name, seats
FROM events
WHERE seats >= 100
ORDER BY seats;

-- 4. WHERE: активные бронирования
SELECT id, event_id, user_id, tickets_count
FROM bookings
WHERE is_cancelled = 0
ORDER BY id;

-- 5. WHERE: отменённые бронирования
SELECT id, event_id, user_id, tickets_count
FROM bookings
WHERE is_cancelled = 1
ORDER BY id;

-- 6. JOIN: активные бронирования с названием мероприятия и именем
SELECT bookings.id, events.name AS event_name, events.date AS event_date,
       users.name AS user_name, bookings.tickets_count,
       bookings.is_cancelled
FROM bookings
JOIN events ON bookings.event_id = events.id
JOIN users ON bookings.user_id = users.id
WHERE bookings.is_cancelled = 0
ORDER BY bookings.id;

-- 7. JOIN: все бронирования по пользователям, включая отменённые
SELECT users.name AS user_name, events.name AS event_name,
       bookings.tickets_count, bookings.is_cancelled
FROM bookings
JOIN users ON bookings.user_id = users.id
JOIN events ON bookings.event_id = events.id
ORDER BY users.name, bookings.id;

-- 8. Мероприятия на дату со свободными местами (подзапрос, JOIN, WHERE)
SELECT e.id, e.name, e.date, e.venue, e.seats, e.price,
       e.seats - COALESCE(b.booked, 0) AS free_seats
FROM events e
LEFT JOIN (
    SELECT event_id, SUM(tickets_count) AS booked
    FROM bookings
    WHERE is_cancelled = 0
    GROUP BY event_id
) b ON e.id = b.event_id
WHERE e.date = '2026-11-20'
  AND e.seats - COALESCE(b.booked, 0) > 0
ORDER BY e.name;

-- 9. COUNT: число активных бронирований
SELECT COUNT(*) AS bookings_count
FROM bookings
WHERE is_cancelled = 0;

-- 10. SUM: число проданных билетов по активным бронированиям
SELECT COALESCE(SUM(tickets_count), 0) AS tickets_sold
FROM bookings
WHERE is_cancelled = 0;

-- 11. GROUP BY: число активных бронирований по мероприятиям
SELECT events.name AS event_name, COUNT(bookings.id) AS bookings_count
FROM events
LEFT JOIN bookings
    ON events.id = bookings.event_id
    AND bookings.is_cancelled = 0
GROUP BY events.id, events.name
ORDER BY bookings_count DESC;

-- 12. GROUP BY + HAVING: мероприятия с более чем одним активным бронированием
SELECT events.name AS event_name, COUNT(bookings.id) AS bookings_count
FROM events
JOIN bookings ON events.id = bookings.event_id
WHERE bookings.is_cancelled = 0
GROUP BY events.id, events.name
HAVING COUNT(bookings.id) > 1
ORDER BY bookings_count DESC;