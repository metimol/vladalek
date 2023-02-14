from django.db import models
from tinymce.models import HTMLField
from account.models import Profile

class Categories(models.Model):
	category = models.CharField(max_length=25,  verbose_name='Категорія', help_text='Назва категорії')
	def __str__ (self):
		return self.category
	class Meta:
		verbose_name = "Категорія"
		verbose_name_plural = "Категорії"

class Articles(models.Model):
	categories = models.ForeignKey(Categories, null=True, related_name = "articles", on_delete = models.SET_NULL, verbose_name='Категорія')
	article_author = models.ForeignKey(Profile, related_name = "articles", on_delete = models.CASCADE, verbose_name='Автор статті')
	article_title = models.CharField(max_length=20, help_text='Введіть назву статті', verbose_name='Назва статті')
	article_text = HTMLField(help_text='Текст статті', verbose_name='Текст статті')
	article_about = models.TextField(help_text='Про що стаття', verbose_name='Опис статті', null=True)
	pub_date = models.DateField(auto_now_add=True)
	fixed = models.BooleanField(default=False, verbose_name="Закріпити")
	favorites = models.ManyToManyField(Profile, related_name="favourites", blank=True, verbose_name = "Обране")
	def __str__(self):
		return self.article_title
	class Meta:
		verbose_name = 'Стаття'
		verbose_name_plural = 'Статті'

class Coments(models.Model):
	articles = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='coments', verbose_name='До якої статті?')
	coment_author = models.ForeignKey(Profile, related_name = "coments", on_delete = models.CASCADE, verbose_name='Автор коментаря')
	coment_text = models.CharField(max_length=200, verbose_name='Текст коментаря')
	pub_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.coment_text
	class Meta:
		verbose_name = 'Коментар'
		verbose_name_plural = 'Коментарі'
