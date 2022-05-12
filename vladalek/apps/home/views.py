from django.shortcuts import render
from blog.models import Articles
from account.models import Profile

def index(request):
	fixed_list = Articles.objects.filter(fixed=True)
	articles_list = Articles.objects.order_by('-id')[:3]
	if Profile.objects.filter(username="metimol").exists():
		admin = Profile.objects.get(username="metimol")
	else:
		admin = None
	context = {'fixed_list': fixed_list, 'articles_list': articles_list, "admin": admin}
	return render(request, 'home/index.html', context,)

def sitemap(request):
	
	return render(request, 'sitemap/sitemap.xml')
