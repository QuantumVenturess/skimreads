from comments.models import Comment
from django.contrib import admin
from readings.models import Note, Reading
from votes.models import Vote

class NoteCommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class NoteVoteInline(admin.TabularInline):
    model = Vote
    extra = 3

class NoteAdmin(admin.ModelAdmin):
    inlines = [NoteCommentInline, NoteVoteInline]
    list_display = ['created', 'content', 'admin_reading', 'admin_user']
    list_filter = ['reading', 'user']
    search_fields = ['content']

class ReadingInline(admin.TabularInline):
    model = Note
    extra = 3

class ReadingAdmin(admin.ModelAdmin):
    inlines = [ReadingInline]
    list_display = ['created', 'title', 'admin_link', 'admin_image', 
        'admin_user', 'views']
    list_filter = ['user']
    search_fields = ['title']

admin.site.register(Note, NoteAdmin)
admin.site.register(Reading, ReadingAdmin)