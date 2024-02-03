from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *
from .destinationform import DestinationForm

# Create your views here.
def home(request):
    return render(request, 'planner/home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def planner_dashboard(request):
    holidays = Holiday.objects.filter(user=request.user).order_by('-start_date')[:3]
    return render(request, 'planner/dashboard.html', { 'holidays': holidays })

@login_required
def holidays_list(request):
    holidays = Holiday.objects.filter(user=request.user)
    return render(request, 'planner/holidays_list.html', { 'holidays': holidays})

class HolidayCreate(LoginRequiredMixin, CreateView):
    model = Holiday
    fields = ['name', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def holidays_detail(request, pk):
    holiday = Holiday.objects.get(id=pk)
    destination_form = DestinationForm()
    return render(request, 'planner/holidays_detail.html', { 'holiday': holiday,'destination_form': destination_form })

@login_required
def destinations_detail(request, holiday_id, destination_id):
    destination = Destination.objects.get(id=destination_id)
    holiday = Holiday.objects.get(id=holiday_id)
    return render(request, 'planner/destination_detail.html', {'destination': destination, 'holiday': holiday})

@login_required
def itinerary_detail(request, destination_id, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    destination = Destination.objects.get(id=destination_id)
    return render(request, 'planner/itinerary_detail.html', {'itinerary':itinerary, 'destination': destination})

class ItinCreate(CreateView):
    model = Itinerary
    fields = ['start_date', 'end_date', 'description']

#    def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     print(kwargs.get('destination_id'))
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        destination_id = self.kwargs.get('destination_id')
        destination = Destination.objects.get(id=destination_id)
        form.instance.destination = destination
        return super().form_valid(form)

    def get_success_url(self):
        destination_id = self.object.destination.id
        holiday_id = self.object.destination.holiday.id
        return reverse_lazy('destinations-detail', kwargs={'holiday_id': holiday_id, 'destination_id': destination_id})

class ItinUpdate(UpdateView):
   model = Itinerary
   fields = ['start_date', 'end_date', 'description']

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
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('planner-dashboard')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)