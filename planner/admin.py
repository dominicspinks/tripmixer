from django.contrib import admin
from .models import Holiday, Destination, Itinerary

# Register your models here.
admin.site.register(Holiday)
admin.site.register(Destination)
admin.site.register(Itinerary)