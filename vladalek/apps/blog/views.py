from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Articles, Coments, Categories
from .forms import ComentForm
from account.models import Profile

def index(request):
	categories = request.GET.get('category', '')
	categories_list = Categories.objects.all()
	if categories:
		try:
			cat = Categories.objects.get(category=categories)
			articles_list = cat.articles.order_by('-id')
			return render(request, "blog/index.html", {"articles_list": articles_list})
		except:
			return render(request, "404.html")
	else:
		return render(request, "blog/categories.html", {"categories": categories_list})

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
