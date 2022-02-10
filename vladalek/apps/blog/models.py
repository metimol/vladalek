from django.db import models
from tinymce.models import HTMLField
from account.models import Profile

class Categories(models.Model):
	category = models.CharField(max_length=25,  verbose_name='Категория', help_text='Название категории')
	def __str__ (self):
		return self.category
	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"

class TemporaryCategories(models.Model):
	category = models.CharField(max_length=25,  verbose_name='Категория', help_text='Название категории')
	category_code = models.TextField(verbose_name='Код')
	def __str__ (self):
		return self.category
	class Meta:
		verbose_name = "Временная категория"
		verbose_name_plural = "Временные категории"

class Articles(models.Model):
	categories = models.ForeignKey(Categories, null=True, related_name = "articles", on_delete = models.SET_NULL, verbose_name='Категория')
	article_author = models.ForeignKey(Profile, related_name = "articles", on_delete = models.CASCADE, verbose_name='Автор статьи')
	article_title = models.CharField(max_length=20, help_text='Введите название статьи', verbose_name='Название статьи')
	article_text = HTMLField(help_text='Текст статьи', verbose_name='Текст статьи')
	article_about = models.TextField(help_text='О чём статья', verbose_name='Описание статьи', null=True)
	pub_date = models.DateField(auto_now_add=True)
	fixed = models.BooleanField(default=False, verbose_name="Закрепить")
	favorites = models.ManyToManyField(Profile, related_name="favourites", blank=True, verbose_name = "Избранное")
	def __str__(self):
		return self.article_title
	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'

class Coments(models.Model):
	articles = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='coments', verbose_name='К какой статье?')
	coment_author = models.ForeignKey(Profile, related_name = "coments", on_delete = models.CASCADE, verbose_name='Автор коментария')
	coment_text = models.CharField(max_length=200, verbose_name='Текст коментария')
	pub_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.coment_text
	class Meta:
		verbose_name = 'Коментарий'
		verbose_name_plural = 'Коментарии'
