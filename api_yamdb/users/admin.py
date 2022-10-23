from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'role', 'confirmation_code',)
    search_fields = ('email', 'username',)
    list_filter = ('role',)
    list_editable = ('email', 'username', 'role', 'confirmation_code',)
    empty_value_display = '-пусто-'
