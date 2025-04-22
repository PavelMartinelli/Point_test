import json
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    CHECK_OUT = 0
    CHECK_IN = 1


@dataclass
class Event:
    date: str
    event_type: EventType


def create_events(guests: list) -> list[Event]:
    events = []
    for guest in guests:
        events.append(Event(guest["check-in"], EventType.CHECK_IN))
        events.append(Event(guest["check-out"], EventType.CHECK_OUT))
    return events


def check_capacity(max_capacity: int, guests: list) -> bool:
    events = create_events(guests)
    sorted_events = sorted(events, key=lambda e: (e.date, e.event_type.value))
    count_guests = 0

    for event in sorted_events:
        if event.event_type == EventType.CHECK_IN:
            count_guests += 1
            if count_guests > max_capacity:
                return False
        else:
            count_guests -= 1
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())

    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)
