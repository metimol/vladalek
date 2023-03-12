from django.shortcuts import render
from blog.models import Articles
from account.models import Profile

def index(request):
	return render(request, 'home/index.html',)

def sitemap(request):
	
	return render(request, 'sitemap/sitemap.xml')
