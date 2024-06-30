from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from .models import User, Profile
from main.models import Post
from django.db.models import Count
from .forms import RegisterForm, PassResetForm
import re 


def signup(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			user_name = request.user.username
			messages.success(request, f'Your account has been created successfuly!')
			return redirect('create-profile', username=user_name)
	else:
		form = RegisterForm()

	# user = authenticate(username=username, password=password1)
	# login(request, user)
	return render(request, 'user/signup.html', {'form': form})



class CreateProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView, UpdateView):
	model = Profile
	# form_class = Profile_form
	template_name = 'user/create-profile.html'
	fields = ['Profile_picture', 'full_name', 'bio', 'tech_stack', 'current_city', 'Website_or_Portfolio_link']
	success_url = reverse_lazy('home')

	def dispatch(self, request, *args, **kwargs):
		username = self.request.user.username
		url_username = self.kwargs.get('username')
		if username != url_username:
			return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset = None):
		return self.request.user.profile

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.user:
			return True
		else:
			return False
		return self.request.user.is_authenticated

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
		messages.success(self.request, self.success_message)

	# def success_url(self):
	# 	return reverse_lazy('home', {'pk':self.object.pk})

class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView, UpdateView):
	model = Profile
	# form_class = Profile_form
	template_name = 'user/edit-profile.html'
	fields = ['Profile_picture', 'full_name', 'bio', 'tech_stack', 'current_city', 'Website_or_Portfolio_link']
	# success_url = reverse_lazy('user-profile', {'username': self.request.user.username})

	def get_success_url(self):
		username = self.kwargs['username']
		return reverse_lazy('user-profile', kwargs={'username': username})

	def dispatch(self, request, *args, **kwargs):
		username = self.request.user.username
		url_username = self.kwargs.get('username')
		if username != url_username:
			return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset = None):
		return self.request.user.profile

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.user:
			return True
		else:
			return False
		return self.request.user.is_authenticated

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
		messages.success(self.request, self.success_message)

class DetailProfileView(LoginRequiredMixin, DetailView):
	model = Profile
	template_name = 'user/profile.html'
	context_object_name = 'profile'
	profiles = Profile.objects.get(user__username = 'justondev')
	bio = profiles.bio
	print(Profile.objects.all())
	if bio == "":
		print("bio is null")
	else:
		print(bio)

	def get_object(self, queryset = None):
		username = self.kwargs.get('username')
		user = User.objects.get(username=username)
		return user.profile

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		posts  = Post.objects.filter(author=self.object).order_by('-date_posted')
		posts = posts.annotate(num_comments = Count('comments'))
		context['posts'] = posts
		context['title'] = 'Profile'
		return context

@login_required
def like_profile(request, profile_id):
	profile = get_object_or_404(Profile, id=profile_id)
	if profile.likes.filter(id=request.user.id).exists():
		profile.likes.remove(request.user)
	else:
		profile.likes.add(request.user)

	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_refer_not_found'))
