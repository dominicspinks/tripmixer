from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Holiday(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('holiday-detail', kwargs={'pk': self.id})

class Destination(models.Model):
    holiday = models.ForeignKey(Holiday,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description=models.TextField(max_length=250, blank=True, default='')

    def __str__(self):
        return self.location
    class Meta:
        ordering = ['-start_date']

    def get_absolute_url(self):
        return reverse('destinations-detail', kwargs={'holiday_id': self.holiday.id, 'destination_id': self.id })

class Itinerary(models.Model):
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('itinerary-detail', kwargs={'itinerary_id': self.id, 'destination_id': self.destination.id})

    # Function to check if the itinerary starts and ends on the same day
    def ends_same_day(self):
        return self.start_date.date() == self.end_date.date()

ACCOM_TYPES = (
    ('Hotels', 'Hotels'),
    ('Hostel', 'Hostels'),
    ('Bed and breakfast', 'Bed and breakfast'),
    ('Guesthouse', 'Guesthouse'),
    ('Airbnb', 'Airbnb'),
    ('Apartments', 'Apartments'),
    ('Resorts', 'Resorts'),
    ('Camping', 'Camping'),
    ('Chalets', 'Chalets')
)

class Accommodation(models.Model):
    itinerary = models.OneToOneField(Itinerary, on_delete=models.CASCADE)
    accom_name = models.CharField(max_length=100)
    accom_type = models.CharField(max_length=20, choices=ACCOM_TYPES, default=ACCOM_TYPES[0][0])
