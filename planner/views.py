from django.shortcuts import render, redirect
from .models import *
from .destinationform import DestinationForm

# Create your views here.
def home(request):
    return render(request, 'planner/home.html')

def about(request):
    return render(request, 'about.html')

def holidays_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'planner/holidays_list.html', { 'holidays': holidays})

def planner_dashboard(request):
    holidays = Holiday.objects.all().order_by('-start_date')[:3]
    return render(request, 'planner/dashboard.html', { 'holidays': holidays })

def holidays_detail(request, pk):
    holiday = Holiday.objects.get(id=pk)
    destination_form = DestinationForm()
    return render(request, 'planner/holidays_detail.html', { 'holiday': holiday,'destination_form': destination_form })

def destinations_detail(request, holiday_id, destination_id):
    destination = Destination.objects.get(id=destination_id)
    return render(request, 'planner/destination_detail.html', {'destination': destination})

def itinerary_detail(request, destination_id, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    return render(request, 'planner/itinerary_detail.html', {'itinerary':itinerary})

def add_destination(request, holiday_id):
    form = DestinationForm(request.POST)
    if form.is_valid():
        new_destination = form.save(commit=False)
        new_destination.holiday_id = holiday_id
        new_destination.save()
    return redirect('holiday-detail',pk=holiday_id)
