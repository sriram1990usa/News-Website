from django import forms
# from django.contrib.auth.models import User
from userauths.models import User
from django.contrib.auth.forms import UserCreationForm
from userauths.models import Profile, User
from django.forms import fields
# from userauths.models import 

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'prompt srch_explore'}), max_length=50, required=True)
    # username = forms.EmailInput(widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=50, required=True)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class profileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name', 'class': 'prompt srch_explore'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Bio', 'class': 'prompt srch_explore'}))
    profile_image = forms.ImageField()
    facebook = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Facebook', 'class': 'prompt srch_explore'}))
    twitter = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Twitter', 'class': 'prompt srch_explore'}))
    linkedin = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin', 'class': 'prompt srch_explore'}))
    youtube = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Youtube', 'class': 'prompt srch_explore'}))

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'profile_image', 'facebook', 'twitter', 'linkedin', 'youtube',]

class userUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'prompt srch_explore'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email', 'class': 'prompt srch_explore'}))

    class Meta:
        model = User
        fields = ['username', 'email']


    
