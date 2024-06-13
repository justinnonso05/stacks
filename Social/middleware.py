from django.shortcuts import redirect
from django.urls import reverse
from user.models import Profile

class ProfileMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		if request.user.is_authenticated:
			profile, created = Profile.objects.get_or_create(user=request.user)
			if created:
				return redirect("create-profile", username = request.user.username)
		return response

# class PasswordResetMIddleware:
# 	def __init__(self, get_response):
# 		self.get_response = get_response

# 	def __call__(self, request):
# 		if request.user.is_authenticated and request.session.get('reset_password'):
# 			if request.path != '/password_reset/':
# 				return redirect('/password_reset/')
# 		response = self.get_response(request)
# 		return response	