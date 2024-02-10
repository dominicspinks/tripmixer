from django.shortcuts import render
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import ImageFormSet
from django.db import transaction
from planner.models import Holiday

import datetime

# Create your views here.
def blog_home(request):
    posts = Post.objects.filter(is_public=True)
    return render(request, 'blog/blog_home.html', { 'posts': posts})

@login_required
def post_list(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'blog/post_list.html', { 'posts': posts})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post_detail.html', { 'post': post })

class PostOwnerMixin(UserPassesTestMixin):
    """
    Mixin to verify that the current user is the owner of the post.
    """
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'holiday', 'description', 'is_public')
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

        # Filter holiday dropdown list by user's holidays
        user_holidays = Holiday.objects.filter(user=self.request.user)
        form.fields['holiday'].queryset = user_holidays
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.create_date = datetime.datetime.now()

        context = self.get_context_data()
        image_formset = context['image_formset']

        with transaction.atomic():
            self.object = form.save()
            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.object.id
        return reverse_lazy('post-detail', kwargs={'post_id': post_id})

class PostUpdate(LoginRequiredMixin, PostOwnerMixin, UpdateView):
    model = Post
    fields = ('title', 'holiday', 'description', 'is_public')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object)
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
        context = self.get_context_data()
        image_formset = context['image_formset']

        with transaction.atomic():
            self.object = form.save()
            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()

        return super().form_valid(form)

    def get_success_url(self):
            post_id = self.object.id
            return reverse_lazy('post-detail', kwargs={'post_id': post_id})


class PostDelete(LoginRequiredMixin, PostOwnerMixin, DeleteView):
    model = Post
    # Add handling of deleting images from S3

    def get_success_url(self):
        return reverse_lazy('post-list')