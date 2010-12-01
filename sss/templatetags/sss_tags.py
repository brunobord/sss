import os
import datetime
from django import template
from django.db.models import Sum
from django.utils.translation import ugettext as _
from sss.models import BacklogItem
from sss.conf.settings import SPRINT_NORMAL_DURATION
from sss.exceptions import EmptyBurndownError

register = template.Library()


@register.simple_tag
def project_summary():
    "Display a simple summary of the project"
    qs = BacklogItem.current.filter(done=False)
    if qs.count():
        return " / ".join((
            _("Tasks remaining %d") % qs.count(),
            _("Remaining points %(story_points__sum)d") % qs.aggregate(Sum('story_points'))
        ))
    else:
        return _("Either your project hasn't started, or it's completely done! Next?")



def burndown_compute():
    "Compute every bit of data needed by the Burndown Chart"
    qs = BacklogItem.current.all()

    if qs.count() == 0:
        raise EmptyBurndownError(_('No backlog, no chart yet'))

    first_date_started = qs.order_by('date_started')[0].date_started
    delta = datetime.datetime.now() - first_date_started
    max_x = SPRINT_NORMAL_DURATION
    if delta.days > SPRINT_NORMAL_DURATION:
        max_x = delta.days

    total_points = qs.aggregate(Sum('story_points'))['story_points__sum']

    x_range = max_x + 1

    ideal_data = []
    current_data = []

    select_date = {'day_done': """strftime('%%Y-%%m-%%d', date_done)"""}

    current_points = qs.extra(select=select_date).values('day_done', 'done').annotate(points=Sum('story_points'))

    for x in range(0, x_range):
        points = total_points - (total_points * (x/float(SPRINT_NORMAL_DURATION + 1)))
        if points > 0:
            ideal_data.append(str(points))
        else:
            ideal_data.append('0')
        # current
        current_day = datetime.datetime(
            first_date_started.year,
            first_date_started.month,
            first_date_started.day, 23, 59, 59) + datetime.timedelta(days=x)
        points = sum(item['points'] for item in current_points if item['day_done'] <= str(current_day) and item['done'])
        current_data.append(str(total_points - points))
        
    ideal_data.append('0')

    # today position
    today_delta = datetime.datetime.now() - first_date_started
    today_position = (today_delta.days * 100) / max_x
    # return data
    return ideal_data, current_data, max_x, total_points, today_position


@register.simple_tag
def project_burndown_google():
    """Display a burndown chart, using Google Chart API. If your network
    connection is down, it won't work."""

    GOOGLE_CHART_URL = ''.join(
        [
            "http://chart.apis.google.com/chart?chs=%(width)dx%(height)d&chtt=%(title)s",
            "&cht=lc&chdl=%(estimated_label)s|%(actual_label)s&chco=FF0000,00FF00",
            "&chds=0,%(max_y)d&chd=t:%(ideal_data)s|%(current_data)s",
            "&chxr=0,0,%(max_x)d,2|1,0,%(max_y)d,%(step_y)d&chxt=x,y,x",
            "&chxl=2:|today|",
            "&chxp=2,%(today_position)d",
            "&chxtc=2,-180",
            "", # TODO: line style
        ])
    BURNDOWN_IMG = '<img src="%s" alt="%s" />'

    try:
        ideal_data, current_data, max_x, total_points, today_position = burndown_compute()
    except EmptyBurndownError, e:
        return e

    burndown_url = GOOGLE_CHART_URL % {
        'ideal_data': ",".join(ideal_data),
        'current_data': ",".join(current_data),
        'max_x': max_x,
        'max_y': total_points,
        'step_y': int(total_points / 5),
        'width': 600, 'height': 250,
        'title': _('Burndown Chart'),
        'estimated_label': _('estimated data'),
        'actual_label': _('actual data'),
        'today_position': today_position,
    }
    return BURNDOWN_IMG % (burndown_url, _('Burndown Chart'))


@register.simple_tag
def project_burndown():
    """Display a burndown chart, using JQuery Flot lib.
    """
    FLOT_STRING = """<div id="placeholder" style="width:%(width)dpx;height:%(height)dpx;"></div>
    <script id="source" language="javascript" type="text/javascript">
        django.jQuery(function () {
            var ideal_data = {data: Array(%(ideal_data)s), label: "%(estimated_label)s", color: "#900"};
            var current_data = {data: Array(%(current_data)s), label: "%(actual_label)s", color: "#090"};
            django.jQuery.plot(django.jQuery("#placeholder"), [ ideal_data, current_data ]);
    });</script> """

    try:
        ideal_data, current_data, max_x, total_points, today_position = burndown_compute()
    except EmptyBurndownError, e:
        return e

    return FLOT_STRING % {
        "width": 600,
        'height': 250,
        'ideal_data': ','.join(r'[ %d, %s ]' % (x, y) for x, y in zip(range(0, max_x+15), ideal_data)),
        'current_data': ','.join(r'[ %d, %s ]' % (x, y) for x, y in zip(range(0, max_x+15), current_data)),
        'estimated_label': _('estimated data'),
        'actual_label': _('actual data'),
    }


@register.simple_tag
def sss_custom_js():
    "A generic custom JS loader"
    directory = os.path.dirname(__file__)
    filepath = os.path.join(directory, 'static', 'jquery.flot.js')
    return open(filepath, "r").read().replace('jQuery', 'django.jQuery')
