from django.urls import path
from .views import index, sitemap

app_name = 'home'
urlpatterns = [
	path('', index, name='index'),
	path("sitemap/", sitemap, name="sitemap"),
]