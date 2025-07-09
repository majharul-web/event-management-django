import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant  # change this

fake = Faker()

def populate():
    # Create Categories
    categories = []
    for _ in range(5):
        name = fake.unique.word().capitalize()
        category = Category.objects.create(
            name=name,
            description=fake.sentence()
        )
        categories.append(category)
    print(f"✅ Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(10):
        date = fake.date_between(start_date='today', end_date='+60d')
        time = fake.time()
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=date,
            time=time,
            location=fake.address(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"✅ Created {len(events)} events.")

    # Create Participants and assign them to random events
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participant.event.set(random.sample(events, random.randint(1, 3)))
        participants.append(participant)
    print(f"✅ Created {len(participants)} participants.")

    print("🎉 Database seeded successfully!")

if __name__ == "__main__":
    populate()
