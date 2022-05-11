import random
import string
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.hashers import make_password, check_password
from .models import Profile
from .forms import LoginForm, RegisterForm, ResetForm, ResetConfirmForm, AvatarForm, DeleteForm
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import requests

def user_login(request):
			
	return render(request, 'account/login.html')

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:index'))

def user_about(request):
	if request.user.is_authenticated:
		user = Profile.objects.get(username = request.user.username)
		bookmark = user.favourites.all()
		articles = user.articles.all()
		if request.method=="POST" and "change_photo" in request.POST:
			form = AvatarForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				avatar = cd['avatar']
				user.avatar = avatar
				user.save()
		
		context = {'user': user, "bookmark": bookmark, "articles": articles}
	else:
		return HttpResponseRedirect(reverse('account:login'))
	
	return render(request, 'account/about.html', context)

def user_delete(request):
	if request.user.is_authenticated:
		user = Profile.objects.get(username = request.user.username)
		if request.method=="POST":
			form = DeleteForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				password = cd['password']
				if check_password(password, user.password):
					user.delete()
					return HttpResponseRedirect(reverse('home:index'))
				else:
					messages.error(request, 'Неверный пароль')
	else:
		return HttpResponseRedirect(reverse('account:login'))
	
	return render(request, 'account/delete.html',)