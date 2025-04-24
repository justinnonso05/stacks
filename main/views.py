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
from django.utils.decorators import method_decorator
from django.core.mail import send_mass_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, get_connection


def landing(request):
	return render(request, 'main/welcome.html')

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

	def get_users(self):
		search_query = self.request.GET.get('key')
		if search_query:
			users = User.objects.filter(Q(username__icontains = search_query.lower()) | Q(profile__bio__icontains = search_query.upper()) | Q(profile__full_name__icontains = search_query.upper()))
		else:
			users = User.objects.none()
		return users


	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Search Results'
		context['users'] = self.get_users()
		return context



def materials(request):
	return render(request, 'main/materials.html', {'title': 'Level Materials'})

def groups(request):
	return render(request, 'main/groups.html', {'title': 'Academic Calendar'})


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
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count(),
    })


@login_required
def liked_posts(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	users = post.likes.all()
	profiles = Profile.objects.filter(user__in=users)
	context = {
		'profiles': profiles,
		'post': post
		}
	return render(request, 'main/liked_posts.html', context)

def superuser_required(user):
	return user.is_superuser or user.is_staff

def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, connection=None):
    connection = connection or get_connection(username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        msg = EmailMultiAlternatives(subject, text, from_email, recipient)
        msg.attach_alternative(html, 'text/html')
        messages.append(msg)
    return connection.send_messages(messages)

@login_required
def send_bulk_email_view(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'error': 'You do not have permission to access this page!'}, status=403)

    subject = 'Hop Back on Our Site!'
    from_email = 'Stacks <thestacks.dev@gmail.com>'

    users = User.objects.all()
    recipient_list = [user.email for user in users]

    messages = []

    for email in recipient_list:
        html_content = render_to_string('main/email.html')
        text_content = strip_tags(html_content)

        messages.append((subject, text_content, html_content, from_email, [email]))

    send_mass_html_mail(messages)

    return JsonResponse({'status': 'Emails sent successfully!'})
