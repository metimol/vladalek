from django.shortcuts import render
from .models import News
from blog.models import Articles
from account.models import Profile

def index(request):
	news_list = News.objects.order_by('-id')
	articles_list = Articles.objects.order_by('-id')[:3]
	if Profile.objects.filter(username="metimol").exists():
		admin = Profile.objects.get(username="metimol")
	else:
		admin = None
	context = {'news_list': news_list, 'articles_list': articles_list, "admin": admin}
	return render(request, 'home/index.html', context,)
