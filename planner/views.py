from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, 'planner/home.html')

def about(request):
    return render(request, 'about.html')

def holidays_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'planner/holidays_list.html', { 'holidays': holidays})

def planner_dashboard(request):
    pass

def holidays_detail(request):
    pass

def destinations_detail(request):
    pass

def itinerary_detail(request):
    pass
