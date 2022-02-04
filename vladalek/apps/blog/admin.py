from django.contrib import admin
from .models import Articles, Coments, Categories, TemporaryCategories

admin.site.register(Articles)
admin.site.register(Coments)
admin.site.register(Categories)
admin.site.register(TemporaryCategories)
