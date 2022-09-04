from django.db import models
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

CREATOR_RATING = (
	(Decimal("1.0"), "★☆☆☆☆ (1/5)"),
	(Decimal("2.0"), "★★☆☆☆ (2/5)"),
	(Decimal("3.0"), "★★★☆☆ (3/5)"),
	(Decimal("4.0"), "★★★★☆ (4/5)"),
	(Decimal("5.0"), "★★★★★ (5/5)"),
)

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    creator = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    normal_user = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# uploading user files to a specific directory
def user_directory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=1000, default="DexxaEd")
	bio = models.CharField(max_length=100, default="DexxaEd User")
	about_me = models.TextField(blank=True, null=True)
	profile_image = models.ImageField(upload_to=user_directory_path, default="default_profile_image.jpg")

	creator = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)
	normal_user = models.BooleanField(default=True)

	address = models.CharField(max_length=1000, null=True, blank=True)
	phone = models.IntegerField(default=0)
	website = models.URLField(default="https://", null=True, blank=True)

	facebook = models.URLField(default="https://", null=True, blank=True)
	twitter = models.URLField(default="https://", null=True, blank=True)
	linkedin = models.URLField(default="https://", null=True, blank=True)
	youtube = models.URLField(default="https://", null=True, blank=True)		
	instagram = models.URLField(default="https://", null=True, blank=True)		

	# favourite = models.ManyToManyField(Course)
	# favourite_tutorial = models.ManyToManyField(Book)

	def __str__(self):
		return self.user.username
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.profile_image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.profile_image.path)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


class CreatorRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="profile")
	rating = models.DecimalField(max_digits=2, decimal_places=1, choices=CREATOR_RATING)
	review = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
	
	def __str__(self):
		return f"{self.profile.full_name} - {self.rating}"
	
	class Meta:
		verbose_name = "Creator Rating"