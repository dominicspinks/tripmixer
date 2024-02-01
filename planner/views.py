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
    return render(request, 'planner/dashboard.html')

def holidays_detail(request, pk):
    holiday = Holiday.objects.get(id=pk)
    return render(request, 'planner/holidays_detail.html', { 'holiday': holiday })

def destinations_detail(request, holiday_id, destination_id):
    destination = Destination.objects.get(id=destination_id)
    return render(request, 'planner/destination_detail.html', {'destination': destination})

def itinerary_detail(request, destination_id, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    return render(request, 'planner/itinerary_detail.html', {'itinerary':itinerary})
