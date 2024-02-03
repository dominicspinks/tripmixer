from django.forms import ModelForm
from .models import Destination
from django.forms import DateInput

class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = ['location','start_date','end_date','description']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }