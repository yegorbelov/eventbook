from models.event import Event
from models.user import User


class Booking:
    def __init__(self, booking_id: int, event: Event, user: User, tickets_count: int) -> None:
        self.id = booking_id
        self.event = event
        self.user = user
        self.tickets_count = tickets_count
        self.is_cancelled = False

    def cancel(self) -> None:
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "отменено" if self.is_cancelled else "подтверждено"
        return (
            f"[{self.id}] {self.user.name} — {self.event.name}, "
            f"билетов: {self.tickets_count}, статус: {status}"
        )
