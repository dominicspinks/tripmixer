from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import *

# Create your views here.
def home(request):
    return render(request, 'planner/home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def holidays_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'planner/holidays_list.html', { 'holidays': holidays})

@login_required
def planner_dashboard(request):
    holidays = Holiday.objects.all().order_by('-start_date')[:3]
    return render(request, 'planner/dashboard.html', { 'holidays': holidays })

@login_required
def holidays_detail(request, pk):
    holiday = Holiday.objects.get(id=pk)
    return render(request, 'planner/holidays_detail.html', { 'holiday': holiday })

@login_required
def destinations_detail(request, holiday_id, destination_id):
    destination = Destination.objects.get(id=destination_id)
    return render(request, 'planner/destination_detail.html', {'destination': destination})

@login_required
def itinerary_detail(request, destination_id, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    destination = Destination.objects.get(id=destination_id)
    return render(request, 'planner/itinerary_detail.html', {'itinerary':itinerary, 'destination': destination})
