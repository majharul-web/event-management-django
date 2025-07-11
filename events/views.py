from django.shortcuts import render, redirect
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm
from datetime import date
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from users.views import is_admin
from django.contrib.auth.models import User

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()



def event_detail(request, pk):
    event = Event.objects.select_related('category').prefetch_related('participants').get(pk=pk)
    return render(request, 'event_detail.html', {'event': event})

# ---------- DASHBOARD ----------
@login_required
def organizer_dashboard(request):
    today = date.today()
    filter_type = request.GET.get('filter', 'all')
    
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    today_events = base_query.filter(date=today).order_by('date')

    # Count distinct participants across all events
    participant_counts = User.objects.filter(rsvped_events__isnull=False).aggregate(
    total_unique_participants=Count('id', distinct=True)
)

    # Filtered event logic
    if filter_type == 'upcoming':
        filtered_events = base_query.filter(date__gt=today).order_by('date')
        title = "Upcoming Events"
    elif filter_type == 'past':
        filtered_events = base_query.filter(date__lt=today).order_by('-date')
        title = "Past Events"
    elif filter_type == 'today':
        filtered_events = base_query.filter(date=today)
        title = "Today's Events"
    else:
        filtered_events = base_query.all().order_by('-date')
        title = "All Events"

    # Event counts
    counts = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events=Count('id', filter=Q(date__gt=today)),
        past_events=Count('id', filter=Q(date__lt=today)),
        today_events=Count('id', filter=Q(date=today))
    )

    context = {
        'counts': counts,
        'today_events': today_events,
        'filtered_events': filtered_events,
        'title': title,
        'total_participants': participant_counts['total_unique_participants'],
    }

    return render(request, 'events/organizer_dashboard.html', context)



# ---------- CATEGORY ----------
@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category created successfully!")
        return redirect('category_list')
    return render(request, 'events/form.html', {'form': form, 'title': 'Add Category'})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('category_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Category'})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('category_list')

    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
    else:
        messages.error(request, "Invalid request method.")
    return redirect('category_list')


# ---------- EVENT ----------

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def event_list(request):
    search = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('participants')
    if search:
        events = events.filter(Q(name__icontains=search) | Q(location__icontains=search))
    return render(request, 'events/event_list.html', {'events': events})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()  
    return render(request, 'events/form.html', {'form': form, 'title': 'Add Event'})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def event_update(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES, instance=event)
        
        print("Files data:", request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Event'})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def event_delete(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
    else:
        messages.error(request, "Invalid request method.")
    return redirect('event_list')

@login_required
def rsvp_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('/')

    # Prevent duplicate RSVP
    if request.user in event.rsvps.all():
        messages.warning(request, "You have already RSVP'd to this event.")
    else:
        event.rsvps.add(request.user)
        messages.success(request, "RSVP successful!")

        # Send confirmation email
        send_mail(
            subject="RSVP Confirmation - Event Manager",
            message=f"Hi {request.user.first_name},\n\nYou've successfully RSVP'd to: {event.name} on {event.date} at {event.time}.\n\nLocation: {event.location}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=True,
        )

    return redirect('event_detail', pk=event.id)


# ---------- PARTICIPANT ----------

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def participant_list(request):
    participants = User.objects.filter(rsvped_events__isnull=False).distinct().prefetch_related('rsvped_events')
    return render(request, 'events/participant_list.html', {
        'participants': participants,
    })

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Participant created successfully!")
        return redirect('participant_list')
    return render(request, 'events/form.html', {'form': form, 'title': 'Add Participant'})

@login_required
def join_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('/')

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            participant.event.add(event)
            messages.success(request, "You have successfully joined the event!")
            return redirect('event_detail', pk=pk)
    else:
        form = ParticipantForm()
        form.fields['event'].initial = [event.id]
        form.fields['event'].disabled = True  

    return render(request, 'form.html', {
        'form': form,
        'title': f"Join: {event.name}",
        'event_id': event.id  
    })

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def participant_update(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        messages.error(request, "Participant not found.")
        return redirect('participant_list')

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully!")
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)

    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Participant'})

@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def participant_delete(request, pk):
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        messages.error(request, "Participant not found.")
        return redirect('participant_list')

    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
    else:
        messages.error(request, "Invalid request method.")
    return redirect('participant_list')

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    return redirect('no-permission')