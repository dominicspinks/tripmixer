from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import *
from .forms import HolidayForm, DestinationForm, ItineraryForm, AccommodationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from blog.models import Post
from django.urls import reverse_lazy

# About page
def about(request):

    return render(request, 'about.html')

# Dashboard
@login_required
def planner_dashboard(request):
    holidays = Holiday.objects.filter(user=request.user).order_by('-start_date')[:3]
    posts = Post.objects.filter(user=request.user).order_by('-create_date')

    return render(request, 'planner/dashboard.html', { 'holidays': holidays, 'posts': posts })

## Holiday pages ##
# List of user's holidays
@login_required
def holidays_list(request):
    holidays = Holiday.objects.filter(user=request.user)

    # Get holiday form for add holiday modal view
    holiday_form = HolidayForm()

    return render(
        request,
        'planner/holidays_list.html',
        {
            'holidays': holidays,
            'holiday_form': holiday_form
        }
    )

# Details of a single holiday
@login_required
def holidays_detail(request, pk):
    holiday = Holiday.objects.get(id=pk)

    # Get holiday form for edit holiday modal view
    holiday_form = HolidayForm(instance=holiday)

    # Get destination form for add destination modal view
    destination_form = DestinationForm()

    return render(
        request,
        'planner/holidays_detail.html',
        {
            'holiday': holiday,
            'destination_form': destination_form,
            'holiday_form': holiday_form
        }
    )

# CBV to handle requests for adding a holiday
class HolidayCreate(LoginRequiredMixin, CreateView):
    model = Holiday
    fields = ['name', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

# CBV to handle requests for updating a holiday
class HolidayUpdate(LoginRequiredMixin, UpdateView):
    model = Holiday
    fields = ['name', 'start_date', 'end_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        holiday = Holiday.objects.get(id=self.object.id)
        context['holiday_form'] = HolidayForm(instance=holiday)

        return context

# CBV to handle delete confirmation and deleting holiday from db
class HolidayDelete(LoginRequiredMixin, DeleteView):
    model = Holiday

    def get_success_url(self):

        return reverse_lazy('holiday-list')

## Destinations ##
# Destination Details page
@login_required
def destinations_detail(request, holiday_id, destination_id):
    destination = Destination.objects.get(id=destination_id)

    # Create form for adding an Itinerary item
    itinerary_form = ItineraryForm()

    # Create form for editing the destination details
    destination_form = DestinationForm(instance=destination)



    return render(
        request,
        'planner/destination_detail.html',
        {
            'destination': destination,
            'itinerary_form': itinerary_form,
            'destination_form': destination_form,
        }
    )

# Handle requests for adding a new holiday
@login_required
def destination_create(request, holiday_id):
    form = DestinationForm(request.POST)

    if form.is_valid():
        new_destination = form.save(commit=False)
        new_destination.holiday_id = holiday_id
        new_destination.save()

    return redirect('holiday-detail',pk=holiday_id)

# CBV to handle updating a destination
class DestinationUpdate(LoginRequiredMixin, UpdateView):
    model = Destination
    fields = ['location', 'start_date', 'end_date', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = Destination.objects.get(id=self.object.id)
        context['destination_form'] = DestinationForm(instance=destination)

        return context

# CBV to handle delete confirmation and deleting a destination from db
class DestinationDelete(LoginRequiredMixin, DeleteView):
    model = Destination

    def get_success_url(self):
        holiday_id = self.object.holiday.id

        return reverse_lazy('holiday-detail', kwargs={'pk': holiday_id})

## Itinerary views ##
# Detail view for a specific itinerary item
@login_required
def itinerary_detail(request, destination_id, itinerary_id):
    itinerary = Itinerary.objects.get(id=itinerary_id)
    # if Accommodation.objects.get(id=itinerary_id):
    #     accommodation = Accommodation.objects.get(id=itinerary_id)

    # Create form for adding an Itinerary item
    itinerary_form = ItineraryForm(instance=itinerary)

    # Create form for adding an accommodation to an itinerary
    accommodation_form = AccommodationForm()

    return render(
        request,
        'planner/itinerary_detail.html',
        {
            'itinerary': itinerary,
            'itinerary_form': itinerary_form,
            'accommodation_form':  accommodation_form
        }
    )

# CBV to handle requests for adding an itinerary item
class ItinCreate(LoginRequiredMixin, CreateView):
    model = Itinerary
    fields = ['start_date', 'end_date', 'description']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        destination_id = self.kwargs.get('destination_id')
        destination = Destination.objects.get(id=destination_id)
        form.instance.destination = destination

        return super().form_valid(form)

    def get_success_url(self):
        destination_id = self.object.destination.id
        itinerary_id = self.object.id

        return reverse_lazy('itinerary-detail', kwargs={'destination_id': destination_id, 'itinerary_id': itinerary_id})

# CBV to handle requests for updating an itinery item
class ItinUpdate(LoginRequiredMixin, UpdateView):
    model = Itinerary
    fields = ['start_date', 'end_date', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itinerary_form'] = ItineraryForm

        return context

# CBV to handle delete confirmation and deleting an itinerary from db
class ItinDelete(LoginRequiredMixin, DeleteView):
    model = Itinerary

    def get_success_url(self):
        destination_id = self.object.destination.id
        holiday_id = self.object.destination.holiday.id

        return reverse_lazy('destination-detail', kwargs={'holiday_id': holiday_id, 'destination_id': destination_id})

## Accommodations ##
# CBV to handle requests for adding a new accommodation item
class AccomCreate(LoginRequiredMixin, CreateView):
    model = Accommodation
    fields = ['accom_name', 'accom_type']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        itinerary_id = self.kwargs.get('itinerary_id')
        itinerary = Itinerary.objects.get(id=itinerary_id)
        form.instance.itinerary = itinerary

        return super().form_valid(form)

    def get_success_url(self):
        destination_id = self.object.itinerary.destination.id
        itinerary_id = self.object.id

        return reverse_lazy('itinerary-detail', kwargs={'destination_id': destination_id, 'itinerary_id': itinerary_id })

# Handle signing up new users
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