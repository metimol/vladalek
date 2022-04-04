from django import forms

class ComentForm(forms.Form):
	text = forms.CharField()

class CreateArticleForm(forms.Form):
	categories = forms.CharField()
	article_title = forms.CharField(max_length=20)
	text_article = forms.CharField()
	article_about = forms.CharField(max_length=100)

class CreateCategoryForm(forms.Form):
	category = forms.CharField()

class EditArticleForm(forms.Form):
	article_title = forms.CharField(max_length=20)
	text_article = forms.CharField()
	article_about = forms.CharField(max_length=100)