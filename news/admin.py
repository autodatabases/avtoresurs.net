from django.contrib import admin

# Register your models here.
from news.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'added', 'updated', 'status')

admin.site.register(Post, PostAdmin)

