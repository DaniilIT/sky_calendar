from django.contrib import admin

from goals.models import GoalCategory


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_deleted')
    list_display_links = ('title',)
    list_editable = ('is_deleted',)
    search_fields = ('title',)
    list_filter = ('is_deleted',)

    raw_id_fields = ('user',)
    readonly_fields = ('created', 'updated')
