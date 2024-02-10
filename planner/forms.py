from django.forms import ModelForm
from .models import Holiday, Destination, Itinerary, Accommodation
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput

class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = ['location','start_date','end_date','description']
        widgets = {
            'start_date': DatePickerInput(
                attrs={
                    "class": "my-exclusive-input"
                    },
                options = {
                    'format': 'DD MMM YYYY'
                }
                ),
            'end_date': DatePickerInput(
                attrs={
                    "class": "my-exclusive-input"
                    },
                options = {
                    'format': 'DD MMM YYYY',
                },
                range_from='start_date'
                ),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date'
        }

class ItineraryForm(ModelForm):
    class Meta:
        model = Itinerary
        fields = ['start_date','end_date','description']
        widgets = {
            'start_date': DateTimePickerInput(
                attrs={"class": "my-exclusive-input"},
                options = {
                    'format': 'DD MMM YYYY, hh:mm A'
                }
            ),
            'end_date': DateTimePickerInput(
                attrs={"class": "my-exclusive-input"},
                options = {
                    'format': 'DD MMM YYYY, hh:mm A'
                },
                range_from='start_date'
            ),
        }
        labels = {
            'start_date': 'Start Date & Time',
            'end_date': 'End Date & Time',
        }

class HolidayForm(ModelForm):
    class Meta:
        model = Holiday
        fields = ['name','start_date','end_date']
        widgets = {
            'start_date': DatePickerInput(
                attrs={
                    "class": "my-exclusive-input"
                    },
                options = {
                    'format': 'DD MMM YYYY'
                }
                ),
            'end_date': DatePickerInput(
                attrs={
                    "class": "my-exclusive-input"
                    },
                options = {
                    'format': 'DD MMM YYYY'
                },
                range_from='start_date'
                ),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date'
        }

class AccommodationForm(ModelForm):
    class Meta:
        model = Accommodation
        fields = ['accom_name','accom_type']
        labels = {
            'accom_name': 'Accommodation Name',
            'accom_type': 'Type'
        }