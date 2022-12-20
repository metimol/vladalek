from django.urls import path
from .views import API

app_name = 'jarvis'
urlpatterns = [
	path('', API.as_view(), name='api'),
]