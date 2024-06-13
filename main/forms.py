from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import SetPasswordForm

class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.pop('autofocus', None)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content', 'comment_image']


