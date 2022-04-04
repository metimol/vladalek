from django.urls import path
from .views import index, detail, coments_list, create_article, create_category, create_category_confirm, edit_article

app_name = 'blog'
urlpatterns = [
	path('', index, name='index'),
	path('<int:article_id>/', detail, name='detail'),
	path('<int:article_id>/coments_list/', coments_list, name='coments_list'),
	path('create_article/', create_article, name='create_article'),
	path('create_category/', create_category, name="create_category"),
	path('create_category/<str:category>/<str:code>', create_category_confirm, name="category_confirm"),
	path('edit_article/<int:title>/', edit_article, name="edit_article"),
]