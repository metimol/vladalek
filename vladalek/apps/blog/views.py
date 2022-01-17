from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Articles, Coments, Categories
from .forms import ComentForm, CreateArticleForm
from account.models import Profile

def index(request):
	category = request.GET.get('category', '')
	page_num = request.GET.get('page', '')
	if category:
		try:
			cat = Categories.objects.get(category=category)
			articles_list = cat.articles.order_by('-id')
		except:
			return render(request, "404.html")
	else:
		articles_list = Articles.objects.order_by('-id')
	if articles_list:
		paginator = Paginator(articles_list, 1)
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
		categories_list = Categories.objects.order_by('category')
		context = {'page': page, 'articles_list': page.object_list, 'categories_list': categories_list, 'category': category, 'paginator': paginator, 'page_list':page_list}
	else:
		return render(request, "404.html")
	
	return render(request, 'blog/index.html', context,)

def detail(request, article_id):
	try:
		a = Articles.objects.get(id = article_id)
	except:
		return render(request, "404.html")
	coments_list = a.coments.order_by('id')[:8]
	if request.method=="POST":
		form = ComentForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			text = cd['text']
			Coments.objects.create(articles=a ,coment_text=text, coment_author=Profile.objects.get(username=request.user.username))
			return HttpResponseRedirect(reverse('blog:detail', args=(a.id,)))
	context = {'a': a, 'coments_list': coments_list}
	
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
				article_text = cd['article_text']
				article_about = cd['article_about']
				Articles.objects.create(categories=Categories.objects.get(category=categories), article_author=Profile.objects.get(username=request.user.username), article_title=article_title, article_text=article_text, article_about=article_about)
		context = {'categories_list': categories_list, 'CreateArticleForm': CreateArticleForm}
	else:
		return HttpResponseRedirect(reverse('account:login'))
	
	return render(request, "blog/create_article.html", context,)
