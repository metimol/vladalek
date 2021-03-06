import random
import string
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password
from .models import Articles, Coments, Categories, TemporaryCategories
from .forms import ComentForm, CreateArticleForm, CreateCategoryForm, EditArticleForm
from account.models import Profile

def index(request):
	category = request.GET.get('category', '')
	page_num = request.GET.get('page', '')
	categories_list = Categories.objects.order_by('category')
	if category:
		try:
			cat = Categories.objects.get(category=category)
			articles_list = cat.articles.order_by('-id')
		except:
			return render(request, "404.html")
	else:
		articles_list = Articles.objects.order_by('-id')
	if articles_list:
		paginator = Paginator(articles_list, 10)
		if not page_num:
			page_num = 1
		page = paginator.get_page(page_num)
		page_list = []
		if paginator.num_pages>1:
			if paginator.num_pages>7:
				if int(page_num)<paginator.num_pages-5:
					for i in range(int(page_num), int(page_num)+5):
						page_list.append(i)
				else:
					for i in range(paginator.num_pages-5, paginator.num_pages):
						page_list.append(i)
			else:
				for i in range(1, paginator.num_pages+1):
					page_list.append(i)
		context = {'page': page, 'articles_list': page.object_list, 'categories_list': categories_list, 'category': category, 'paginator': paginator, 'page_list':page_list}
	else:
		return render(request, "blog/index.html", {"categories_list": categories_list})
	
	return render(request, 'blog/index.html', context,)

def detail(request, article_id):
	try:
		a = Articles.objects.get(id = article_id)
	except:
		return render(request, "404.html")
	coments_list = a.coments.order_by('id')[:8]
	if request.method=="POST" and "add_coment" in request.POST:
		form = ComentForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			text = cd['text']
			Coments.objects.create(articles=a ,coment_text=text, coment_author=Profile.objects.get(username=request.user.username))
			return HttpResponseRedirect(reverse('blog:detail', args=(a.id,)))
	elif request.method=="POST" and "add_favourite" in request.POST:
		if request.user.is_authenticated:
			if request.user in a.favorites.all():
				a.favorites.remove(request.user)
			else:
				a.favorites.add(request.user)
		else:
			return HttpResponseRedirect(reverse('account:login'))
	if request.user in a.favorites.all():
		fav = True
	else:
		fav = False
	context = {'a': a, 'coments_list': coments_list, "fav": fav}
	
	return render(request, 'blog/detail.html', context,)

def coments_list(request, article_id):
	try:
		a = Articles.objects.get(id = article_id)
	except:
		return render(request, "404.html")
	coments_list = a.coments.all()
	paginator = Paginator(coments_list, 20)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {"page": page, "coments_list": page.object_list, "a": a}
	
	return render(request, "blog/coments_list.html", context,)

def create_article(request):
	if request.user.is_authenticated:
		categories_list = Categories.objects.order_by('category')
		if request.method=="POST":
			form = CreateArticleForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				categories = cd['categories']
				article_title = cd['article_title']
				article_text = cd['text_article']
				article_about = cd['article_about']
				Articles.objects.create(categories=Categories.objects.get(category=categories), article_author=Profile.objects.get(username=request.user.username), article_title=article_title, article_text=article_text, article_about=article_about)
				return HttpResponseRedirect(reverse('blog:index'))
		context = {'categories_list': categories_list, 'CreateArticleForm': CreateArticleForm}
	else:
		return HttpResponseRedirect(reverse('account:login'))
	
	return render(request, "blog/create_article.html", context,)

def generate_code():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(20))

def create_category(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			form = CreateCategoryForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				category = cd['category']
				if len(category)<20:
					if not Categories.objects.filter(category=category).exists():
						if not TemporaryCategories.objects.filter(category=category).exists():
							code = generate_code()
							TemporaryCategories.objects.create(category=category, category_code=make_password(code))
							text = f"???????????????????????? {request.user.username} ?????????? ?????????????? ?????????????????? {category}"
							url = f"http://127.0.0.1:8000/blog/create_category/{category}/{code}"
							msg_html = render_to_string('account/email.html', {'username': 'Metimol', 'text': text, 'url': url, 'for_admin': True})
							email = "rdgo16480@gmail.com"
							send_mail('???????????????? ??????????????????', text, 'Metimol', [email], html_message=msg_html,)
							return HttpResponseRedirect(reverse('blog:index'))
						else:
							messages.error(request, "?????? ?????????????????? ?????? ?????????????????????????????? ?????? ????????????????????")
					else:
						messages.error(request, "?????????? ?????????????????? ?????? ????????????????????")
				else:
					messages.error(request, "?????????? ???????????????? ???? ???????????? 20 ????????????????")
	else:
		return HttpResponseRedirect(reverse('account:login'))
	
	return render(request, "blog/create_category.html",)
		
def create_category_confirm(request, category, code):
	try:
		c = TemporaryCategories.objects.get(category=category)
	except:
		return render(request, "404.html")
	if check_password(code, c.category_code):
		Categories.objects.create(category=c.category)
		c.delete()
		return HttpResponseRedirect(reverse('home:index'))

def edit_article(request, title):
	try:
		article = Articles.objects.get(id=title)
	except:
		return render(request, "404.html")
	if request.user.is_authenticated and request.user==article.article_author:
		if request.method=="POST":
			form = EditArticleForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				article_title = cd['article_title']
				article_text = cd['text_article']
				article_about = cd['article_about']
				article.article_title, article.article_text, article.article_about = article_title, article_text, article_about
				article.save()
				return HttpResponseRedirect(reverse('account:about'))
		context = {'article': article}
	else:
		return render(request, "404.html")
	
	return render(request, "blog/edit_article.html", context,)
		
