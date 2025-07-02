## Shell Commands for Event Management Project

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Migrations

```bash
python manage.py makemigrations
```

### Create data for events management system

```bash

# create category
from events.models import *
Category.objects.create(name='Music', description='All music events')
Category.objects.create(name='Sports', description='All sports events')
Category.objects.create(name='Arts', description='All arts events')

# get all categories
categories = Category.objects.all()

# create event
from datetime import date, time
Event.objects.create(
    name="AI Summit 2025",
    description="An event focused on AI advancements.",
    date=date(2025, 8, 15),
    time=time(14, 30),
    location="Dhaka International Convention Center",
    category=categories[0]
)
Event.objects.create(
    name="Tech Expo 2025",
    description="A technology exhibition showcasing the latest innovations.",
    date=date(2025, 9, 20),
    time=time(10, 0),
    location="Bangabandhu International Conference Center",
    category=categories[0]
)
Event.objects.create(
    name="Art Festival 2025",
    description="A festival celebrating various forms of art.",
    date=date(2025, 10, 5),
    time=time(11, 0),
    location="National Art Gallery",
    category=categories[2]
)
Event.objects.create(
    name="Football Championship 2025",
    description="A championship for football enthusiasts.",
    date=date(2025, 11, 10),
    time=time(16, 0),
    location="Bangabandhu National Stadium",
    category=categories[1]
)

# get all events
events = Event.objects.all()

# create participant and register them for events
Participant.objects.create(name='John Doe',
    email='john.doe@example.com'
)
Participant.objects.create(name='Jane Smith',
    email='jane.smith@example.com'
)
Participant.objects.create(name='Alice Johnson',
    email='alice.johnson@example.com'
)
Participant.objects.create(name='Bob Brown',
    email='bob.brown@example.com'
)

# register participants for events
event1 = Event.objects.get(name="AI Summit 2025")
event2 = Event.objects.get(name="Tech Expo 2025")
event3 = Event.objects.get(name="Art Festival 2025")

participant1 = Participant.objects.get(name='John Doe')
participant2 = Participant.objects.get(name='Jane Smith')
participant3 = Participant.objects.get(name='Alice Johnson')

event1.participants.add(participant1, participant2)
event2.participants.add(participant2, participant3)
event3.participants.add(participant1, participant3)
```
