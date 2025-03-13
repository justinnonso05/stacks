from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from user.models import Profile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO


def resize_image(image):
	img = Image.open(image)
	output_size = (700, 700)
	img.thumbnail(output_size)

	output = BytesIO()
	img.save(output, format='PNG', quality=100)
	output.seek(0)

	resized_image = InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}_post.png", 'image/png', output.tell(), None)
	return resized_image

class Post(models.Model):
	author = models.ForeignKey(Profile, on_delete = models.CASCADE)
	Post_image = models.ImageField(blank = True, null = True, default = None, verbose_name = "Add Image", upload_to = 'Post_images')
	date_posted = models.DateTimeField(default = timezone.now)
	content = models.TextField()
	likes = models.ManyToManyField(User, related_name='liekd_posts', blank=True)

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return f'{self.content[:10]} Post'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.Post_image:
			temp = self.Post_image
			self.Post_image = resize_image(temp)
			super().save(*args, **kwargs)
			temp.delete(save=False)
		else:
			super().save(*args, **kwargs)

	# def get_absolute_url(self):
	# 	return reverse('post-detail', kwargs={'slug': self.slug})
		

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
	user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
	comment_image = models.ImageField(blank = True, null = True, default = None, verbose_name = "Add Image", upload_to = 'Post_images')
	date_commented = models.DateTimeField(default = timezone.now)
	content = models.TextField()

	def __str__(self):
		return f'{self.content[:10]} Comment'

	def get_post(self):
		return self.post

