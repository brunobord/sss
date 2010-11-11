from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _

class BacklogItem(models.Model):

    STORY_POINT_CHOICES = ((x, x) for x in (0, 1, 2, 3, 5, 8, 13, 20, 40, 100))

    label = models.CharField(_('label'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    priority = models.PositiveIntegerField(_('priority'), default=0,
        help_text=_("Please rank this item. The highest score means it's the"
        " top most priority"))
    story_points = models.PositiveIntegerField(_('story points'),
        choices=STORY_POINT_CHOICES,
        help_text=_("Story points describe the relative difficulty of each task"))
    done = models.BooleanField(_('done'), default=False,
        help_text=_("Check this if you've done the task"))
    date_created = models.DateTimeField(_('date created'), default=datetime.now)
    date_modified = models.DateTimeField(_('date modified'), default=datetime.now)

    class Meta:
        verbose_name = _('backlog item')
        verbose_name_plural = _('backlog items')

    def __unicode__(self):
        return self.label

    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        super(BacklogItem, self).save()