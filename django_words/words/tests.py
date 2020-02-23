import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Word


class WordModelTests(TestCase):
    def test_was_added_recently_with_future_word(self):
        """
        was_added_recently() returns False for word whose added_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_word = Word(added_date=time)
        self.assertIs(future_word.was_added_recently(), False)

    def test_was_added_recently_with_words_older_than_1_day(self):
        """
        was_added_recently() returns False for word whose added_date
        older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_word = Word(added_date=time)
        self.assertIs(future_word.was_added_recently(), False)

    def test_was_added_recently_with_word_within_1_day(self):
        """
        was_added_recently() returns True for word whose added_date
        is within 1 day from now.
        """
        time = timezone.now() - (
            datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        )
        future_word = Word(added_date=time)
        self.assertIs(future_word.was_added_recently(), True)
