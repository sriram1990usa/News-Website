from django import forms
from base.models import Comments, Article

class CreateArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		exclude = ('status', 'slug', 'date', 'views', 'creator')
		# fields = ['full_name', 'email', 'comment']