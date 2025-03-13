from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO

def resize_image(image):
	img = Image.open(image)
	output_size = (350, 350)
	img.thumbnail(output_size)

	output = BytesIO()
	img.save(output, format='PNG', quality=100)
	output.seek(0)

	resized_image = InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}_profile.png", 'image/png', output.tell(), None)
	return resized_image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	verified = models.BooleanField(default=False)
	full_name = models.CharField(max_length = 200)
	Profile_picture = models.ImageField(blank = True, null = True, default = '', upload_to = 'profile_pics')
	bio = models.TextField(max_length = 150, default = "", blank = True, null = True)
	tech_stack = models.CharField(max_length =100, default = "", blank = True, null = True)
	current_city = models.CharField(max_length = 100, default = "", blank = True, null = True)
	# social_link = models.URLField(default = "", blank = True, null = True)
	Website_or_Portfolio_link = models.URLField(default = "", blank = True, null = True)
	likes = models.ManyToManyField(User, related_name='liked_profile', blank=True)

	def total_likes(self):
		return self.likes.count()


	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if self.Profile_picture:
			self.Profile_picture = resize_image(self.Profile_picture)
			super().save(*args, **kwargs)
		super().save(*args, **kwargs)


# run makemigrations & migrations
		