from django.forms import ModelForm, inlineformset_factory
from .models import Post, Image

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

ImageFormSet = inlineformset_factory(
    Post,
    Image,
    form=ImageForm,
    can_delete=False,
    max_num=5, # Max number of formsets allowed
    extra=1    # Number of formsets to render
)