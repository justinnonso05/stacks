from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from .models import Post, Comment
from user.models import Profile
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender = User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Stacks"
        message = f"Welcome to stacks, {instance.username}!\n\nWe're thrilled to have you join our community of developers, tech enthusiasts and innovators. At stacks, we aim to create a space where you can share knowledge, collaborate on projects, and grow together.\n\nAs we are just getting started, your active participation is crucial to our success. Engage with posts, share your insights, and connect with others to help Stacks strive. Together we can build a vibrant and supportive community.\n\nWelcome aboard!\n\nThe Stacks Team\nhttps://stacks.pythonanywhere.com"
        recipient_list = [instance.email]
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, recipient_list)

@receiver(m2m_changed, sender=Post.likes.through)
def send_like_notification(sender, instance, action, **kwargs):
    if action == "post_add":
        subject = "Your post was liked"
        message = f"Your post at https://stacks.pythonanywhere.com/posts/{instance.id}/{instance.author.user.username}/ was liked"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.author.user.email]
        send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender = Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        subject = "New comment on your post"
        message = f"Your post at https://stacks.pythonanywhere.com/posts/{instance.post.id}/{instance.post.author.user.username}/ received a new comment"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.post.author.user.email]
        send_mail(subject, message, from_email, recipient_list)

@receiver(m2m_changed, sender=Profile.likes.through)
def send_prolike_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        liker_ids = list(pk_set)
        likers = User.objects.filter(id__in=liker_ids)

        for liker in likers:
            subject = 'Your Profile was Liked'
            message = f'Hello @{instance.user.username},\n\nYour profile was liked by @{liker.username}.\n\nView your profile https://stacks.pythonanywhere.com/{instance.user.username}/profile/'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.user.email]

            send_mail(subject, message, from_email, recipient_list)