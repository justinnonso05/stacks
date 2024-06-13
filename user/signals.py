# from django.db.models.signals import post_save
# # , user_logged_in
# from django.contrib.auth.models import User
# from django.shortcuts import redirect
# from django.dispatch import receiver
# from .models import Profile

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
# 		instance.profile.save()



# @receiver(user_logged_in)
# def user_logged_in_handler(sender, request, user, **kwargs):
#     if not Profile.objects.filter(user=user).exists():
#         return redirect('create_profile')  # Redirect to profile creation page if profile is not complete
