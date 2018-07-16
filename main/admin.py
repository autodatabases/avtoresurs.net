from django.contrib import admin
from main.models import ArrivalItem


class GoodItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'added', 'active')


admin.site.register(ArrivalItem, GoodItemAdmin)
