from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from userauths.forms import UserRegisterForm, profileUpdateForm, userUpdateForm
from userauths.models import Profile, Follow
from django.conf import settings
from decimal import Decimal
from taggit.managers import TaggableManager
from userauths.models import User
# User = settings.AUTH_USER_MODEL
from base.models import Article

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('email')

            messages.success(request, f'Hurray your account was created!!')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('base:index')
            


    elif request.user.is_authenticated:
        return redirect('base:index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)

# @login_required
def profile(request, username):
    # user = User.objects.get(username=username)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    # favourite = profile.favourite.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    followers_count = Follow.objects.filter(following=user).count()
    articles = Article.objects.filter(creator=user, status="published")
    context = {
        'profile':profile,
        'articles':articles,
        
    }
    return render(request, 'userauths/profile.html', context)



@login_required
def profileUpdate(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = userUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return redirect('profile', request.user)
    else:
        p_form = profileUpdateForm(instance=request.user.profile)
        u_form = userUpdateForm(instance=request.user)
    
    

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'userauths/profile-update.html', context)


# @login_required
# def follow(request, username, option):
#     user = request.user
#     following = get_object_or_404(User, username=username)


#     try:
#         f, created = Follow.objects.get_or_create(follower=request.user, following=following)

#         if int(option) == 0:
#             f.delete()
#             # Stream.objects.filter(following=following, user=request.user).all().delete()
#         else:
#             # elements = Elements.objects.all().filter(creator=following)
#             pass
            
#         # return HttpResponseRedirect(reverse('profile', args=[username]))
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
#     except User.DoesNotExist:
#         # return HttpResponseRedirect(reverse('profile', args=[username]))
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
