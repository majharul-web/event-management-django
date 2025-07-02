from django.shortcuts import render, redirect
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

def home(request):
    categories = Category.objects.all()

    # --- Filters from query parameters ---
    search = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # --- Optimized event query ---
    events = Event.objects.select_related('category').prefetch_related('participants').all()

    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )

    if category_id:
        events = events.filter(category_id=category_id)

    if date_from:
        events = events.filter(date__gte=date_from)

    if date_to:
        events = events.filter(date__lte=date_to)

    context = {
        'events': events,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
        'date_from': date_from,
        'date_to': date_to,
    }

    return render(request, 'home.html', context)

def event_detail(request, pk):
    event = Event.objects.select_related('category').prefetch_related('participants').get(pk=pk)
    return render(request, 'event_detail.html', {'event': event})

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    today = date.today()

    all_events = Event.objects.select_related('category').prefetch_related('participants')
    total_events = all_events.count()
    total_participants = Participant.objects.count()
    total_categories = Category.objects.count()

    upcoming_events = all_events.filter(date__gt=today)
    past_events = all_events.filter(date__lt=today)
    today_events = all_events.filter(date=today)

    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'upcoming':
        filtered_events = upcoming_events
        title = "Upcoming Events"
    elif filter_type == 'past':
        filtered_events = past_events
        title = "Past Events"
    elif filter_type == 'today':
        filtered_events = today_events
        title = "Today's Events"
    else:
        filtered_events = all_events
        title = "All Events"

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'total_categories': total_categories,
        'today_events': today_events,
        'filtered_events': filtered_events,
        'title': title,
        'filter_type': filter_type,
    }
    return render(request, 'events/dashboard.html', context)


# ---------- CATEGORY ----------
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category created successfully!")
        return redirect('category_list')
    return render(request, 'events/form.html', {'form': form, 'title': 'Add Category'})

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
def event_list(request):
    search = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('participants')
    if search:
        events = events.filter(Q(name__icontains=search) | Q(location__icontains=search))
    return render(request, 'events/event_list.html', {'events': events})

def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Event created successfully!")
        return redirect('event_list')
    return render(request, 'events/form.html', {'form': form, 'title': 'Add Event'})

def event_update(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Event'})

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


# ---------- PARTICIPANT ----------
def participant_list(request):
    search_query = request.GET.get('q', '')
    participants = Participant.objects.all()

    if search_query:
        participants = participants.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        )

    paginator = Paginator(participants, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events/participant_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Participant created successfully!")
        return redirect('participant_list')
    return render(request, 'events/form.html', {'form': form, 'title': 'Add Participant'})

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
