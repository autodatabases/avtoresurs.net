from django.contrib import admin

# Register your models here.
from assortment.models import AssortmentItem


class AssortmentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated', 'status')


admin.site.register(AssortmentItem, AssortmentItemAdmin)

