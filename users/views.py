from django.shortcuts import render
from django.contrib.auth.models import Group
from users.forms import SignUpModelForm,SignInModelForm,AssignRoleForm,CreateGroupForm,EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.shortcuts import redirect,get_object_or_404
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
from django.views.generic import TemplateView,UpdateView,ListView,View
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView,LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



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

class SignUpView(View):
    template_name = 'auth/signup.html'

    def get(self, request):
        form = SignUpModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # wait for activation
            user.save()
            messages.success(request, "Account created successfully! Please check your email for activation link.")
            return redirect('sign-in')
        else:
            messages.error(request, "Please correct the errors below.")
            
        return render(request, self.template_name, {'form': form})



# Customized login view
class CustomLoginView(LoginView):
    form_class = SignInModelForm
    
    def get_success_url(self):
        next_url= self.request.GET.get('next')
        
        return next_url if next_url else super().get_success_url()    
    


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
    
    

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')
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

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'auth/password_reset_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['host'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password reset link sent to your email.")
        return response


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name = 'auth/password_reset.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been reset successfully. You can now sign in.")
        return response

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



@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class AssignRoleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'
    login_url = 'sign-in'
    template_name = 'admin/assign_role.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = AssignRoleForm()
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove existing roles
            user.groups.add(role)  # Assign new role
            messages.success(request, f"Role changed to {role} for {user.username}.")
            return redirect('admin-dashboard')
        return render(request, self.template_name, {'user': user, 'form': form})
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class CreateGroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.add_group'
    login_url = 'sign-in'
    template_name = 'admin/create_group.html'

    def get(self, request):
        form = CreateGroupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('create-group')
        else:
            messages.error(request, "Error creating group. Please try again.")
            return render(request, self.template_name, {'form': form})

@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()