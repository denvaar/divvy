from django.contrib import admin

from .models import Account, BaseUser, AppUser


class AppUserAdmin(admin.ModelAdmin):
    exclude = ['groups', 'user_permissions', 'is_staff']

admin.site.register(Account)
admin.site.register(BaseUser)
admin.site.register(AppUser, AppUserAdmin)

