from django.contrib import admin

from goals.models import Goal, GoalCategory, GoalComment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted')
    list_display_links = ('title',)
    list_editable = ('is_deleted',)
    search_fields = ('title',)
    list_filter = ('is_deleted',)

    raw_id_fields = ('user',)
    readonly_fields = ('created', 'updated')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'status', 'due_date')
    list_display_links = ('title',)
    list_editable = ('priority', 'status')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'status', 'due_date')

    raw_id_fields = ('user', 'category')
    readonly_fields = ('created', 'updated')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'goal')
    list_display_links = ('text',)
    search_fields = ('text',)

    raw_id_fields = ('user', 'goal')
    readonly_fields = ('created', 'updated')
