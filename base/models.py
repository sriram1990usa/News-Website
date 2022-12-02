from django.db import models
from django.conf import settings
from decimal import Decimal
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL

STATUS = (
	("draft", "draft"),
	("disabled", "Disabled"),
	("rejected", "Rejected"),
	("in_review", "In Review"),
	("published", "Published"),
)

RATING = (
    (Decimal("1.0"), "★☆☆☆☆ (1/5)"),
    (Decimal("2.0"), "★★☆☆☆ (2/5)"),
    (Decimal("3.0"), "★★★☆☆ (3/5)"),
    (Decimal("4.0"), "★★★★☆ (4/5)"),
    (Decimal("5.0"), "★★★★★ (5/5)"),
)

def user_directory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.creator.id, filename)

def reverse(x):
		t=len(x)
		y=len(x)-1
		z=""
		for i in range(t):
			z+=x[y]
			y-=1
		return z

class Category(models.Model):
	thumbnail = models.ImageField(upload_to="course_category_images")
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=100, null=True, blank=True)
	active = models.BooleanField(default=True)
	slug = models.SlugField(unique=True)
	date = models.DateTimeField(auto_now_add=True)
 	
	def get_absolute_url(self):
		return reverse("", args=[self.slug])

	def __str__(self):
		return self.title 

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

class Article(models.Model):
	thumbnail = models.ImageField(upload_to="thumbnail")
	title = models.CharField(max_length=1000)
	content = models.TextField()
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	read_time = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(unique=True)
	tags = TaggableManager()
	status = models.CharField(choices=STATUS, max_length=100, default="in_review")
	trending = models.BooleanField(default=False)
	featured = models.BooleanField(default=False)
	top_headlines = models.BooleanField(default=False)
	breaking_news = models.BooleanField(default=False)
	popular = models.BooleanField(default=False)
	editors_choice = models.BooleanField(default=False)
	hot = models.BooleanField(default=False)
	weekly_favourite = models.BooleanField(default=False)
	today_headlines = models.BooleanField(default=False)
	
	class Meta:
		verbose_name = "Article"
		verbose_name_plural = "Articles"

	def __str__(self):
		return self.title

	def __str__(self):
		return self.title[0:30]

class Comments(models.Model):
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
	article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, related_name="article")
	full_name = models.CharField(max_length=200)
	email = models.EmailField()
	# rating = models.DecimalField(max_digits=2, decimal_places=1, choices=RATING)
	comment = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
		
	def __str__(self):
		return f"{self.article.title} - {self.rating}"
	
	class Meta:
		verbose_name = "Comment"
		verbose_name_plural = "Comments"

	def __str__(self):
		return self.article.title[0:30]