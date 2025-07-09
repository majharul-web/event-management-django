from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def no_permission(request):
    messages.error(request, "You do not have permission to access this page.")
    return render(request, 'no_permission.html')