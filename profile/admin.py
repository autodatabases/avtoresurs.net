from django.contrib import admin

# Register your models here.
from profile.models import Profile,  Discount


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'vip_code', 'fullname', 'group')
    list_display_links = ('__str__', 'vip_code', 'fullname', 'group')
    search_fields = ('fullname', 'vip_code')
    exclude = ('discount',)



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Discount)
