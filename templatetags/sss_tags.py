from django import template
from django.db.models import Sum
from django.utils.translation import ugettext as _
from sss.models import BacklogItem


register = template.Library()

@register.simple_tag
def project_summary():
    qs = BacklogItem.objects.filter(done=False)
    if qs.count():
        return " / ".join((
            _("Tasks remaining %d") % qs.count(),
            _("Remaining points %(story_points__sum)d") % qs.aggregate(Sum('story_points'))
        ))
    else:
        return _("Either your project hasn't started, or it's completely done! Next?")
