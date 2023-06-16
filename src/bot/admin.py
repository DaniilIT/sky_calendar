from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'user')
    search_fields = ('tg_username', 'user__username')
    readonly_fields = ('chat_id', 'verification_code')
