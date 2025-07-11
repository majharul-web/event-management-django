from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    asset = models.ImageField(upload_to='event_asset/', blank=True, null=True,default='event_asset/default_event.jpg')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    rsvps = models.ManyToManyField(User, related_name='rsvped_events', blank=True)

    def __str__(self):
        return self.name

class Participant(models.Model):  
    name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name

# Admin credential