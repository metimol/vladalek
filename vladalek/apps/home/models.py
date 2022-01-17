from django.db import models

class News(models.Model):
	new_title = models.CharField(max_length=30, verbose_name='Название новости')
	new_text = models.TextField(verbose_name='Текст новости')
	pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата новости')
	def __str__(self):
		return self.new_title
	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'
