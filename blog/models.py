from django.db import models
from django.urls import reverse
from django.apps import apps
import uuid

# import planner.models as Planner_Models
from django.contrib.auth.models import User

# Function to add random string to start of image file names to avoid duplicate names in S3
def prepend_filename(instance, filename):
    return f"blog_images/{uuid.uuid4().hex[:8]}-{filename}"

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holiday = models.ForeignKey('planner.Holiday', null=True, on_delete=models.SET_NULL, default=None)
    destination = models.ForeignKey('planner.Destination', null=True, on_delete=models.SET_NULL, default=None)
    itinerary = models.ForeignKey('planner.Itinerary', null=True, on_delete=models.SET_NULL, default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, default='')
    create_date = models.DateTimeField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'post_id': self.id})

class Image(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=prepend_filename)

    def __str__(self):
        return 'ImageField'