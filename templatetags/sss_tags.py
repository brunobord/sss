import datetime
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


@register.simple_tag
def project_burndown_url():
    qs = BacklogItem.objects.all()
    first = qs.order_by('date_created')[0]

    total_points = qs.aggregate(Sum('story_points'))['story_points__sum']

    ideal_data = []
    current_data = []
    for x in range(0, 14):
        points = total_points - (total_points * (x/14.0))
        ideal_data.append(str(points))
        # current
        current_day = first.date_created + datetime.timedelta(days=x)
        points = qs.filter(done=True, date_modified__lte=current_day).aggregate(Sum('story_points'))['story_points__sum']
        if points is None:
            points = 0
        current_data.append(str(total_points - points))
    ideal_data.append('0')

    return "http://chart.apis.google.com/chart?chs=600x250&chtt=Burndown&cht=lc&chdl=estimated|actual&chco=FF0000,00FF00&chxr=0,0,30,2|1,0,40,2&chds=0,40&chd=t:%(ideal_data)s|%(current_data)s" % {'ideal_data': ",".join(ideal_data), 'current_data': ",".join(current_data)}
