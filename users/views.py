from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from users.forms import SignUpModelForm,SignInModelForm,AssignRoleForm,CreateGroupForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from events.models import Event
from datetime import date
from django.db.models import Q,Count
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

User = get_user_model()

# Create your views here.

def is_admin(user):
    # return user.is_authenticated and user.is_staff
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    form = SignUpModelForm()
    if request.method == 'POST':
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False 
            user.save()
            messages.success(request, "Account created successfully! Please check your email for activation link.")
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'auth/signup.html', {"form": form})


def sign_in(request):
    form=SignInModelForm()
    if request.method == 'POST':
        form = SignInModelForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print("Invalid credentials")

    return render(request, 'auth/signin.html', {"form": form})


@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def activate_account(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        if user.is_active:
            messages.info(request, "Account is already activated.")
            return redirect('sign-in')
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully! You can now sign in.")
            return redirect('sign-in')
        else:
            messages.error(request, "Invalid activation link.")
            return redirect('sign-in')
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('sign-up')
    
# Profile view
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name() or user.username
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        context['phone_number'] = user.phone_number
        if user.profile_image:
            context['profile_image'] = user.profile_image.url
        else:
            context['profile_image'] = 'profile_images/default.png'
        return context

@user_passes_test(is_admin, login_url='no-permission')
def user_list(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')  
    )

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
            
    return render(request, 'admin/user_list.html', {'users': users})

@user_passes_test(is_admin, login_url='no-permission')  
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')  
    )

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    
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
        'users': users
    }
    return render(request, 'admin/admin_dashboard.html', context)


@user_passes_test(is_admin, login_url='no-permission') 
def assign_role(request, user_id):
    user = User.objects.get(pk=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form= AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Clear existing roles
            user.groups.add(role) # Assign new role
            messages.success(request, f"Role changed to {role} for {user.username}.")
            return redirect('admin-dashboard')
        
    return render(request, 'admin/assign_role.html', {'user': user, 'form': form})

@user_passes_test(is_admin, login_url='no-permission') 
def create_group(request):
    form =CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create-group')
        else:
            messages.error(request, "Error creating group. Please try again.")

    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission') 
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

