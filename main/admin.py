from django.contrib import admin

# Register your models here.
from main.models import Slider


class SliderAdmin(admin.ModelAdmin):
    list_display = ('caption', 'text', 'updated', 'order', 'image')


admin.site.register(Slider, SliderAdmin)
