import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Word


class WordModelTests(TestCase):

    def test_was_added_recently_with_future_word(self):
        """
        was_added_recently() returns False for word whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_word = Word(added_date=time)
        self.assertIs(future_word.was_added_recently(), False)