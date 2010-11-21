from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _

from sss.managers import CurrentSprintManager

class BacklogItem(models.Model):
    """A Backlog Item is a task, a feature wanted for the project you're
    building.
    
    You'll have to rate it on two scales:
        * priority - the highest, the most important it is
        * story points - represents relative load and/or difficulty to perform
          or implement the feature. 
    """

    STORY_POINT_CHOICES = ((x, x) for x in (0, 1, 2, 3, 5, 8, 13, 20, 40, 100))

    label = models.CharField(_('label'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    priority = models.PositiveIntegerField(_('priority'), default=0, unique=True,
        help_text=_("Please rank this item. The highest score means it's the"
        " top most priority"))
    story_points = models.PositiveIntegerField(_('story points'),
        choices=STORY_POINT_CHOICES,
        help_text=_("Story points describe the relative difficulty of each task"))
    done = models.BooleanField(_('done'), default=False,
        help_text=_("Check this if you've done the task"))
    current_sprint = models.BooleanField(_('current sprint'), default=False)
    date_created = models.DateTimeField(_('date created'), default=datetime.now)
    date_modified = models.DateTimeField(_('date modified'), default=datetime.now)
    date_started = models.DateTimeField(_('date started'), default=None, blank=True, null=True)
    date_done = models.DateTimeField(_('date done'), default=None, blank=True, null=True)
    
    objects = models.Manager()
    current = CurrentSprintManager()

    class Meta:
        verbose_name = _('backlog item')
        verbose_name_plural = _('backlog items')

    def __unicode__(self):
        return self.label

    def save(self, force_insert=False, force_update=False):
        now = datetime.now()
        if self.date_created == None:
            self.date_created = now
        if not force_update:
            # if forced by manual action on queryset / object
            self.date_modified = now
            if self.date_done is None and self.done:
                self.date_done = now
            if self.date_started is None and self.current_sprint:
                self.date_started = now
        
        super(BacklogItem, self).save(force_insert, force_update)
