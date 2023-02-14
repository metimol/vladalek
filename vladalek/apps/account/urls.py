from django.urls import path
from .views import user_login, user_logout, user_about

app_name = "account"
urlpatterns = [
	path('', user_about, name='about'),
	path('login/', user_login, name="login"),
	path('logout/', user_logout, name="logout"),
]