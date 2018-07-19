from django.contrib import admin

# Register your models here.
from news.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'added', 'updated', 'status')
    list_display_links = ('title', 'added', 'updated', 'status')
    list_editable = ('category',)

admin.site.register(Post, PostAdmin)

