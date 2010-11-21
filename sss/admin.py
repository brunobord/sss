from django.contrib import admin
from django.utils.translation import ugettext as _
from sss.models import BacklogItem

# Action(s)
def mark_as_done(modeladmin, request, queryset):
    "Mark every checked backlog item as 'done'"
    queryset.update(done=True)
mark_as_done.short_description = _("Mark these items as done")

def mark_as_current_sprint(modeladmin, request, queryset):
    "Assign every checked backlog item to the current sprint"
    queryset.update(current_sprint=True)
mark_as_current_sprint.short_description = _('Assign these items to current sprint')

def unmark_as_current_sprint(modeladmin, request, queryset):
    "Remove every checked backlog item from the current sprint"
    queryset.update(current_sprint=False)
unmark_as_current_sprint.short_description = _('Unassign these items out of the current sprint')

class BacklogItemAdmin(admin.ModelAdmin):
    "Admin class for Backlog Items"
    ordering = ('-priority',)
    list_display = ['label', 'current_sprint', 'priority', 'story_points', 'done', 'date_done']
    list_filter = ('done', 'current_sprint')
    readonly_fields = ('date_created', 'date_modified', 'date_done')
    actions = [mark_as_done, mark_as_current_sprint, unmark_as_current_sprint]

admin.site.register(BacklogItem, BacklogItemAdmin)
