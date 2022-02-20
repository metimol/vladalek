from django.urls import path
from .views import user_login, user_logout, user_register, user_activate, password_reset, reset_confirm, user_about, user_delete

app_name = "account"
urlpatterns = [
	path('', user_about, name='about'),
	path('login/', user_login, name="login"),
	path('logout/', user_logout, name="logout"),
	path('register/', user_register, name='register'),
	path('<str:username>/<str:code>/', user_activate, name="activate"),
	path('password_reset/', password_reset, name="reset"),
	path('<str:username>/<str:code>/reset/', reset_confirm, name="reset_confirm"),
	path('<str:username>/delete/', user_delete, name="delete"),
]