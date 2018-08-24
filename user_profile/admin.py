from django.contrib import admin

# Register your models here.
from user_profile.models import UserProfile, Discount


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'vip_code', 'fullname', 'group', 'points', 'created', 'updated')
    list_display_links = ('__str__', 'vip_code', 'fullname', 'group')
    search_fields = ('fullname', 'vip_code', 'user__username')
    exclude = ('discount',)


admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Discount)
