from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy, Token
from rest_framework.authtoken.admin import TokenAdmin

User = get_user_model()

admin.site.unregister(Group)

admin.site.unregister(TokenProxy)
admin.site.register(Token, TokenAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
    list_filter = ('username', 'email')
