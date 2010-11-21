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

    def setUp(self):
        self.today = datetime.date.today()
        self.item = BacklogItem(label='task 1', priority=1, story_points=1)
        self.item.save()

    def test_save_creation_date(self):
        self.assertSameDay(self.item.date_created, self.today)
        self.assertSameDay(self.item.date_modified, self.today)

    def test_update_created(self):
        self.item.date_created = datetime.date(2010, 10, 10)
        self.item.save(force_update=True)
        self.assertNotSameDay(self.item.date_created, self.today)

    def test_save_date_done(self):
        self.assertFalse(self.item.date_done)
        self.item.done = True
        self.item.save()
        self.assertSameDay(self.item.date_done, self.today)

    def test_update_done(self):
        self.item.done = True
        self.item.date_done = datetime.date(2010, 10, 10)
        self.item.save(force_update=True)
        self.assertNotSameDay(self.item.date_done, self.today)

    def test_save_date_started(self):
        self.assertFalse(self.item.date_started)
        self.item.current_sprint = True
        self.item.save()
        self.assertSameDay(self.item.date_started, self.today)
        
    def test_update_started(self):
        self.item.current_sprint = True
        self.item.date_started = datetime.date(2010, 10, 10)
        self.item.save(force_update=True)
        self.assertNotSameDay(self.item.date_started, self.today)
