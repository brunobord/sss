from django.contrib import admin
from django.utils.translation import ugettext as _
from sss.models import BacklogItem

# Action(s)
def mark_as_done(modeladmin, request, queryset):
    "Mark every checked backlog item as 'done'"
    queryset.update(done=True)
mark_as_done.short_description = _("Mark these items as done")

class BacklogItemAdmin(admin.ModelAdmin):
    "Admin class for Backlog Items"
    ordering = ('-priority',)
    list_display = ['label', 'priority', 'story_points', 'done', 'date_created', 'date_modified']
    list_filter = ('done',)
    readonly_fields = ('date_created', 'date_modified')
    actions = [mark_as_done]

admin.site.register(BacklogItem, BacklogItemAdmin)
