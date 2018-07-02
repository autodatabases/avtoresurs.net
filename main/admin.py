from django.contrib import admin
from main.models import GoodItem


class GoodItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'active', 'added')


admin.site.register(GoodItem, GoodItemAdmin)
