import sqlite3
from contextlib import closing
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DB = BASE_DIR / "data" / "eventbook.sqlite"

SAMPLE_ROWS = 3


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    uri = f"{SOURCE_DB.as_uri()}?mode=ro"

    with closing(sqlite3.connect(uri, uri=True)) as connection:
        connection.row_factory = sqlite3.Row

        tables = [
            row["name"]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )
        ]

        for table in tables:
            print(f"\nТаблица: {table}")
            print("Столбцы:")
            for column in connection.execute(f'PRAGMA table_info("{table}")'):
                print(
                    f"  имя={column['name']}, тип={column['type']}, "
                    f"NOT NULL={column['notnull']}, "
                    f"PRIMARY KEY={column['pk']}"
                )

            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]
            print(f"Количество записей: {count}")

            print(f"Первые записи (до {SAMPLE_ROWS}):")
            for row in connection.execute(
                f'SELECT * FROM "{table}" ORDER BY 1 LIMIT {SAMPLE_ROWS}'
            ):
                print("  ", dict(row))

        if {"events", "users", "bookings"} <= set(tables):
            check_integrity(connection)


def check_integrity(connection: sqlite3.Connection) -> None:
    """Проверяем, что внешние ключи бронирований не «висят»."""
    print("\nПроверка ссылочной целостности:")

    orphan_events = connection.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        WHERE event_id NOT IN (SELECT id FROM events)
        """
    ).fetchone()[0]
    orphan_users = connection.execute(
        """
        SELECT COUNT(*)
        FROM bookings
        WHERE user_id NOT IN (SELECT id FROM users)
        """
    ).fetchone()[0]
    statuses = connection.execute(
        """
        SELECT is_cancelled, COUNT(*)
        FROM bookings
        GROUP BY is_cancelled
        """
    ).fetchall()

    print(f"  бронирований с несуществующим event_id: {orphan_events}")
    print(f"  бронирований с несуществующим user_id: {orphan_users}")
    print(
        "  значения is_cancelled: "
        + ", ".join(f"{row[0]!r}: {row[1]}" for row in statuses)
    )


if __name__ == "__main__":
    main()
