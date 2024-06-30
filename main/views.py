from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import User, Post, Comment
from user.models import Profile
from .forms import CommentForm
import os
from django.conf import settings
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required


def landing(request):
	return render(request, 'main/landing.html')

class HomeView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'main/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	# paginate_by = 2

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Home'
		return context

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.annotate(num_comments = Count('comments'))
		return queryset

class CreatePostView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'main/create-post.html'
	fields = ['content', 'Post_image']
	context_object_name = 'post'
	success_url = '/'


	def get_object(self, queryset = None):
		return self.request.user.profile.post

	def form_valid(self, form):
		form.instance.author = self.request.user.profile
		messages.success(self.request, 'Your post was added!')
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'New post'
		return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'main/detail-post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post'
        context['comment_form'] = CommentForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_comments=Count('comments'))
        return queryset

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            post = get_object_or_404(Post, pk=request.POST.get('post_id'))
            comment = comment_form.save(commit=False)
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk, username=request.user.username)
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = comment_form
            return self.render_to_response(context)



class MessageView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'main/messages.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Photos'
		return context



class SearchResultView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'main/search.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

	def test_func(self):
		return self.request.user.is_authenticated

	def get_queryset(self):
		queryset = super().get_queryset()
		search_query = self.request.GET.get('key')
		if search_query:
			queryset = queryset.filter(Q(content__icontains = search_query.lower()) | Q(author__full_name__icontains = search_query.upper()))
		queryset = queryset.annotate(num_comments = Count('comments'))
		return queryset

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Search Results'
		return context



def materials(request):
	return render(request, 'main/materials.html', {'title': 'Level Materials'})

def calendar(request):
	return render(request, 'main/calendar.html', {'title': 'Academic Calendar'})


class UpdatePostView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Post
	fields = ['content', 'Post_image']
	template_name = 'main/edit.html'
	context_object_name = 'post'
	success_url = '/'
	success_message = 'Post Edited'

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.author.user:
			return True
		else:
			return False
		return self.request.user.is_authenticated

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Edit post'
		return context

class DeletePostView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Post
	template_name = 'main/delete.html'
	context_object_name = 'post'
	success_url = '/'
	success_message = 'Post Deleted'

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.author.user:
			return True
		else:
			return False
		return self.request.user.is_authenticated

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Delete Post'
		return context

def announcement(request):
	return render(request, 'main/announcement.html', {'title': 'Level Materials'})

@login_required
def like_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
	else:
		post.likes.add(request.user)

	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_refer_not_found'))


# wow