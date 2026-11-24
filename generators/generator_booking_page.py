from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta
import random
from faker import Faker

fake = Faker('ru_RU')

@dataclass(frozen=True)
class BookingData:
    room: str
    date: str
    start_time: str
    end_time: str
    participants: str
    name: str
    email: str

ROOM_CAPACITIES = {
    "small": 4,
    "medium": 10,
    "large": 20,
}

ROOM_LABELS = {
    "small": "Малая",
    "medium": "Средняя",
    "large": "Большая",
}

def generate_booking_data(**kwargs) -> BookingData:
    random_date = (date.today() + timedelta(days=random.randint(1, 30))).isoformat()
    start_time = datetime.now()
    room = kwargs.get("room") or random.choice(list(ROOM_CAPACITIES))
    max_participants = ROOM_CAPACITIES[room]
    default = BookingData(
        room=room,
        date=random_date,
        start_time=start_time.strftime("%H:%M"),
        end_time=(start_time + timedelta(minutes=random.randint(1, 240))).strftime("%H:%M"),
        participants=str(random.randint(1, max_participants)),
        name=fake.first_name(),
        email=fake.email(),
    )
    return replace(default, **kwargs)