from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout
from .models import Profile
from .forms import AvatarForm

def user_login(request):
	return render(request, 'account/login.html')

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:index'))

def user_about(request):
	if request.user.is_authenticated:
		user = Profile.objects.get(username = request.user.username)
		bookmark = user.favourites.all()
		if request.method=="POST" and "change_photo" in request.POST:
			form = AvatarForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				avatar = cd['avatar']
				user.avatar = avatar
				user.save()
		context = {'user': user, "bookmark": bookmark}
	else:
		return HttpResponseRedirect(reverse('account:login'))
	return render(request, 'account/about.html', context)