from django.contrib import admin

# Register your models here.
from main.models import Slide, Slider


# class SlideAdmin(admin.ModelAdmin):
#     list_display = ('caption', 'text', 'updated', 'order', 'image')

admin.site.register(Slide)
admin.site.register(Slider)

