from django.db import models

class CurrentSprintManager(models.Manager):
    def get_query_set(self):
        return super(CurrentSprintManager, self).get_query_set().filter(current_sprint=True)
