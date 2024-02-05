from django.shortcuts import render
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ImageFormSet
from django.db import transaction

import datetime

# Create your views here.
def blog_home(request):
    posts = Post.objects.filter(is_public=True)
    return render(request, 'blog/blog_home.html', { 'posts': posts})

def post_list(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'blog/post_list.html', { 'posts': posts})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post_detail.html', { 'post': post })

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'holiday', 'description', 'is_public')
    # Change this to direct to detail page after creation
    success_url = reverse_lazy('post_list')
    # Destination and itinery tags to be added later, the destination dropdown will need to filter based on the selected holiday, and the itinerary dropdown will need to filter based on the selected destination

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['holiday'].required = False
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.create_date = datetime.datetime.now()

        with transaction.atomic():
            self.object = form.save()
            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()

        context = self.get_context_data()
        image_formset = context['image_formset']


        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'holiday', 'description', 'is_public')
    # Add handling of

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['holiday'].required = False
        return form

    def get_success_url(self):
            post_id = self.object.id
            return reverse_lazy('post-detail', kwargs={'post_id': post_id})


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    # Add handling of deleting imageurl table rows

    def get_success_url(self):
        return reverse_lazy('post-list')