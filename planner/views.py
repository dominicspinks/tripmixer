from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .destinationform import DestinationForm

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
    destination_form = DestinationForm()
    return render(request, 'planner/holidays_detail.html', { 'holiday': holiday,'destination_form': destination_form })

@login_required
def destinations_detail(request, holiday_id, destination_id):
    destination = Destination.objects.get(id=destination_id)
    return render(request, 'planner/destination_detail.html', {'destination': destination})

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)