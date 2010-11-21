import datetime
from django.test import TestCase
from sss.models import BacklogItem

class DateTestCase(TestCase):
    "Tool to compare dates and datetimes"
    def assertSameDay(self, date1, date2):
        self.assertEquals(
            (date1.year, date1.month, date1.day),
            (date2.year, date2.month, date2.day)
        )
    
    def assertNotSameDay(self, date1, date2):
        self.assertNotEquals(
            (date1.year, date1.month, date1.day),
            (date2.year, date2.month, date2.day)
        )


class SaveTest(DateTestCase):
    
    def test_save_creation_date(self):
        today = datetime.date.today()
        item = BacklogItem(label='task 1', priority=1, story_points=1)
        item.save()
        self.assertSameDay(item.date_created, today)
        self.assertSameDay(item.date_modified, today)
        
    def test_force_update(self):
        today = datetime.date.today()
        item = BacklogItem(label='task 1', priority=1, story_points=1)
        item.save()
        item.date_created = datetime.date(2010, 10, 10)
        item.save(force_update=True)
        self.assertNotSameDay(item.date_created, today)
