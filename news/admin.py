from django.contrib import admin

# Register your models here.
from news.models import Post

admin.site.register(Post)
