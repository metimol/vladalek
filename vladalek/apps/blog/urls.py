from django.urls import path
from .views import index, detail, coments_list, create_article

app_name = 'blog'
urlpatterns = [
	path('', index, name='index'),
	path('<int:article_id>/', detail, name='detail'),
	path('<int:article_id>/coments_list/', coments_list, name='coments_list'),
	path('create_article/', create_article, name='create_article'),
]