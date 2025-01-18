from django.db import models
from django.urls import reverse
from django.conf import settings
import uuid
from django.contrib.auth.models import User

def prepend_filename(instance, filename):
    """
    Generates a unique filename
    """
    return f"{uuid.uuid4().hex[:8]}-{filename}"

def prepend_aws_filename(instance, filename):
    """
    Generates a unique filename based on the storage type.
    - For storebytes: No subfolders are used.
    - For AWS S3: Files are placed in the 'blog_images/' subfolder.
    """
    return f"blog_images/{prepend_filename(filename)}"

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
    if settings.IMAGE_STORAGE_TYPE == 'storebytes':
        image = models.ImageField(upload_to=prepend_filename)
    elif settings.IMAGE_STORAGE_TYPE == 'aws_s3':
        image = models.ImageField(upload_to=prepend_aws_filename)

    def __str__(self):
        return 'ImageField'