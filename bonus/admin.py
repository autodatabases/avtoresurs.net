from django.contrib import admin

# Register your models here.
from bonus.models import Bonus


class BonusAdmin(admin.ModelAdmin):
    list_display = ('id_1c', 'title', 'price', 'created_at','updated_at')


admin.site.register(Bonus, BonusAdmin)
