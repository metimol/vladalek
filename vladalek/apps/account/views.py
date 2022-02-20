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
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username'].lower()
			password = cd['password']
			try:
				if '@' in username:
					user = Profile.objects.get(email=username)
				else:
					user = Profile.objects.get(username=username)
				if user is not None and user.is_active and check_password(password, user.password):
					login(request, user)
					return HttpResponseRedirect(reverse('home:index'))
				else:
						messages.error(request, "Неверный логин или пароль")
			except:
				messages.error(request, "Неверный логин или пароль")
	return render(request, 'account/login.html')

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:index'))

def generate_code():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(20))

def user_register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username']
			email = cd['email']
			password = cd['password']
			password2 = cd['password2']
			language = True
			if len(username)>3 and len(username)<21:
				for i in username:
					if ord(i)>128:
						language = False
						break
				if language==True and ' ' not in username:
					if '@' in email:
						if len(password)>6:
							if password == password2:
								if not Profile.objects.filter(username=username.lower()).exists():
									if not Profile.objects.filter(email=email).exists():
										user_code = generate_code()
										Profile.objects.create(username=username.lower(), email=email, password=make_password(password), code=make_password(user_code), is_active=False)
										text = "Пожалуйста, подтвердите Ваш аккаунт на сайте Vladalek."
										url = f"http://127.0.0.1:8000/account/{username}/{user_code}"
										msg_html = render_to_string('account/email.html', {'username': username, 'text': text, 'url': url})
										send_mail('Подтверждение аккаунта', text, 'Metimol', [email], html_message=msg_html,)
										return render(request, "account/url.html")
									else:
										messages.error(request, 'Эта почта уже используется другим аккаунтом')
								else:
									messages.error(request, 'Такой пользователь уже существует')
							else:
								messages.error(request, 'Вы неправильно повторили пароль')
						else:
							messages.error(request, 'Длина пароля не меньше 7 символов')	
					else:
						messages.error(request, 'В адресе электронной почты должен быть символ @')
				else:
					messages.error(request, 'Только латинские буквы (без пробелов) и символы')
			else:
				messages.error(request, 'Длина логина от 4 до 20 символов')
								
	return render(request, "account/register.html")

def user_activate(request, username, code):
	try:
		user = Profile.objects.get(username=username.lower())
		if user.is_active==False and check_password(code, user.code):
			user.is_active = True
			user.code = None
			user.save()
			login(request, user)
			return HttpResponseRedirect(reverse('home:index'))
		else:
			return render(request, "404.html")
	except:
		return render(request, "404.html")

def password_reset(request):
	if request.method == 'POST':
		form = ResetForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			username = cd['username']
			try:
				if '@' in username:
					user = Profile.objects.get(email=username)
				else:
					user = Profile.objects.get(username=username.lower())
				text = "Для сброса пароля перейдите по ссылке."
				code = generate_code()
				user.code = make_password(code)
				user.save()
				url = f'http://127.0.0.1:8000/account/{user.username}/{code}/reset'
				msg_html = render_to_string('account/email.html', {'username': user.username, 'text': text, 'url': url})
				send_mail('Сброс пароля', text, 'Metimol', [user.email], html_message=msg_html,)
				return render(request, "account/url.html")
			except:
				messages.error(request, 'Такого аккаунта не существует')
	return render(request, 'account/reset_password.html')

def reset_confirm(request, username, code):
	try:
		user = Profile.objects.get(username=username.lower())
		if user.is_active==True and check_password(code, user.code):
			if request.method == 'POST':
				form = ResetConfirmForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					password = cd['password']
					password2 = cd['password2']
					if password==password2:
						code = code
						user.code = None
						user.password = password
						user.save()
						login(request, user)
						return HttpResponseRedirect(reverse('home:index'))
					else:
						messages.error(request, 'Вы неправильно повторили пароль')
		else:
			return render(request, "404.html")
	except:
		return render(request, "404.html")
	
	return render(request, 'account/reset_confirm.html')

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

def user_delete(request, username):
	if request.user.is_authenticated:
		if request.user.username==username:
			user = Profile.objects.get(username = request.user.username)
			if request.method=="POST":
				form = DeleteForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					password = cd['password']
					if check_password(password, user.password):
						user.delete()
					else:
						messages.error(request, 'Неверный пароль')
		else:
			return HttpResponseRedirect(reverse('account:login'))
	else:
		return HttpResponseRedirect(reverse('account:login'))
	
	return render(request, 'account/delete.html',)