from datetime import date, datetime, timedelta
import random

MAX_TIME = timedelta(hours=13)  # From 09:00 - 22:00

now = datetime.utcnow()


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

start_date = date(2020, 1, 1)
end_date = date(2021, 1, 1)
start_hour = 9
stop_hour = start_hour + 13

slots = []
for i in range(1,4):
    for j in range(1,26):
        slots.append(f"F{i}_{j}")

slots_avail = {slot:"available" for slot in slots}

for single_date in daterange(start_date, end_date):
    for dt in datetime_range(
        datetime(single_date.year, single_date.month, single_date.day, start_hour),
        datetime(single_date.year, single_date.month, single_date.day, stop_hour),
        timedelta(minutes=1)
        ):
        weekday = dt.weekday()
        hour = dt.hour

        if hour < 10:
            weights = [0.9, 0.1] if weekday < 5 else [0.8, 0.2]
        elif hour >= 10 and hour < 13:
            weights = [0.3, 0.7] if weekday < 5 else [0.2, 0.8]
        elif hour >= 13 and hour < 17:
            weights = [0.4, 0.6] if weekday < 5 else [0.3, 0.7]
        elif hour >= 17 and hour <= 19:
            weights = [0.2, 0.8] if weekday < 5 else [0.1, 0.9]
        elif hour > 19 and  hour <= 20:
            weights = [0.4, 0.6] if weekday < 5 else [0.3, 0.7]
        elif hour > 20 and hour <= 21:
            weights = [0.8, 0.2] if weekday < 5 else [0.9, 0.1]
        elif hour >= 21 and hour < 22:
            weights = [0.9, 0.1]
        else:
            weights = [1.0, 0.0]

        for slot in slots:
            avail = random.choices(['available', 'occupied'], weights=weights)
            if slots_avail[slot] == avail[0]:
                print(slot+','+avail[0]+','+str(dt))
            else:
                slots_avail[slot] = avail[0]
                print(slot+','+avail[0]+','+str(dt))

