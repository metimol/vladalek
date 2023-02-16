from django.contrib import admin
from django.urls import path, include

urlpatterns = [
		path('grappelli/', include('grappelli.urls')),
		path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('account/', include('account.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('jarvis/', include('jarvis.urls')),
]

handler404 = "vladalek.views.page_not_found_view"
