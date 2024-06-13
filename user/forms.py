from django import forms
# from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.pop('autofocus', None)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class PassResetForm(forms.Form):
	username = forms.CharField(max_length=150)
	password1 = forms.CharField(label='New Password', widget = forms.PasswordInput)
	password2 = forms.CharField(label='Confirm new Password', widget = forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")