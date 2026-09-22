class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"
