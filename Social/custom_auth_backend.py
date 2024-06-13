# from django.contrib.auth.backends import ModelBackend

# class CustomAuthBackend(ModelBackend):
# 	def authenticate(self, request, username=None, password=None, **kwargs):
# 		user = super().authenticate(request, username, password, **kwargs)
# 		if user and user.username == password:
# 			request.session['reset_password'] = True

# 		return user