from django.forms import ModelForm
from .models import Destination, Itinerary
from django.forms import DateInput
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = ['location','start_date','end_date','description']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
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
                }
            ),
        }
        labels = {
            'start_date': 'Starting Date & Time',
            'end_date': 'Ending Date & Time',
        }
