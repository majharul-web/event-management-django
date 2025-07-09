from django.urls import path
from . import views

urlpatterns = [

    
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/join/', views.join_event, name='join_event'),


    #Organizer Dashboard
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer_dashboard'),

    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('add-event/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Participant URLs
    path('participants/', views.participant_list, name='participant_list'),
    path('participants/add/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/edit/', views.participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
   


    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    path('dashboard/', views.dashboard, name='dashboard'), 
    
     
]
