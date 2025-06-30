from django.urls import path
from events.views import home, about

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
]