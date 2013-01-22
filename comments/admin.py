from comments.models import Comment
from django.contrib import admin
from replies.models import Reply

class CommentInline(admin.TabularInline):
    model = Reply
    extra = 1

class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['created', 'content', 'admin_note', 'reply_count', 
        'admin_user']
    list_filter = ['user']
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)