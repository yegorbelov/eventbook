class Event:
    def __init__(
        self, event_id: int, name: str, date: str, venue: str, seats: int, price: float
    ) -> None:
        self.id = event_id
        self.name = name
        self.date = date
        self.venue = venue
        self.seats = seats
        self.price = price

    def has_capacity(self, booked_seats: int, tickets_count: int) -> bool:
        return self.seats - booked_seats >= tickets_count

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.name} — {self.venue}, {self.date}, "
            f"мест: {self.seats}, цена: {self.price} руб."
        )
