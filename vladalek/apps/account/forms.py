from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	
class RegisterForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	email = forms.CharField(widget=forms.EmailInput)

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = Profile
		fields = ('username',)

class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = Profile
		fields = ('username',)

class ResetForm(forms.Form):
	username = forms.CharField()

class ResetConfirmForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

class AvatarForm(forms.Form):
	avatar = forms.CharField()