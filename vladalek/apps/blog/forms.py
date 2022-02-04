from django import forms
from tinymce.widgets import TinyMCE

class ComentForm(forms.Form):
	text = forms.CharField()

class CreateArticleForm(forms.Form):
	categories = forms.CharField()
	article_title = forms.CharField(max_length=20)
	article_text = forms.CharField(widget = TinyMCE(attrs={'cols': 80, 'rows': 30}))
	article_about = forms.CharField(max_length=100)

class CreateCategoryForm(forms.Form):
	category = forms.CharField()