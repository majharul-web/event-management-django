
from django.shortcuts import render
from django.contrib import messages
from events.models import Category, Event
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
# ---------- HOME PAGE ----------
def home(request):
    categories = Category.objects.all()

    # Filters from query parameters ---
    search = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # base query for events
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

@login_required
def participant_dashboard(request):
    participant_events = (
        Event.objects
        .select_related('category')
        .prefetch_related('rsvps')
        .filter(rsvps=request.user)
    )
    return render(request, 'participant_dashboard.html', {'participant_events': participant_events})


def event_detail(request, pk):
    event = Event.objects.select_related('category').prefetch_related('participants').get(pk=pk)
    return render(request, 'event_detail.html', {'event': event})

def about(request):
    return render(request, 'about.html')

def no_permission(request):
    messages.error(request, "You do not have permission to access this page.")
    return render(request, 'no_permission.html')