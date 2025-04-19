import json
from datetime import date

def check_capacity(max_capacity: int, guests: list) -> bool:
    bookings = []

    for guest in guests:
        check_in, check_out = date.fromisoformat(guest["check-in"]), date.fromisoformat(guest["check-out"])
        bookings.append((check_in, 1))
        bookings.append((check_out, -1))

    bookings.sort(key=lambda x: (x[0], x[1]))

    current = 0
    for _, delta in bookings:
        current += delta
        if current > max_capacity:
            return False

    return True

if __name__ == "__main__":
    max_capacity = int(input())
    guest_count = int(input())
    guests = [json.loads(input()) for _ in range(guest_count)]
    result = check_capacity(max_capacity, guests)
    print(result)