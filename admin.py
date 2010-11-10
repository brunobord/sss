from django.contrib import admin
from sss.models import BacklogItem

class BacklogItemAdmin(admin.ModelAdmin):
    ordering = ('-priority',)
    list_display = ['label', 'priority', 'story_points', 'done']
    list_filter = ('done',)
    readonly_fields = ('date_created', 'date_modified')
    

admin.site.register(BacklogItem, BacklogItemAdmin)
