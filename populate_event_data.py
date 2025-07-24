import os
import django
import random
from datetime import timedelta
from faker import Faker

# Django environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant

fake = Faker()

def seed_database():
    print("🌱 Seeding the database...")


    # ✅ Create Categories
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.unique.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(category)
    print(f"✅ Created {len(categories)} categories.")

    # ✅ Create Events (no RSVPs at this point)
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=3),
            date=fake.date_between(start_date='today', end_date='+60d'),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories),
            # asset uses default if not provided
        )
        events.append(event)
    print(f"✅ Created {len(events)} events.")

    # ✅ Create Participants and assign random events
    # participants = []
    # for _ in range(20):
    #     participant = Participant.objects.create(
    #         name=fake.name(),
    #         email=fake.unique.email(),
    #     )
    #     # If Participant has ManyToManyField to Event
    #     assigned_events = random.sample(events, k=random.randint(1, 3))
    #     participant.event.set(assigned_events)
    #     participants.append(participant)
    # print(f"✅ Created {len(participants)} participants with event assignments.")

    print("🎉 Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
