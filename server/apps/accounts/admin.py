from django.contrib import admin

from .models import Account, BaseUser, AppUser


class AppUserAdmin(admin.ModelAdmin):
    exclude = ['groups', 'user_permissions', 'is_staff']

class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('account_balance',)
    exclude = ['balance']

    def account_balance(self, obj):
        return '${:2,.2f}'.format(obj.balance)
    
    account_balance.label = 'Balance'

admin.site.register(Account, AccountAdmin)
admin.site.register(BaseUser)
admin.site.register(AppUser, AppUserAdmin)

