from django.contrib import admin

# Register your models here.
from account.models import Account, Point

class AccountAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'vip_code', 'fullname')

admin.site.register(Account, AccountAdmin)
admin.site.register(Point)