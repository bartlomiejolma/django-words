import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_word(word_text, days):
    """
    Create a word with the given `word_text` and published the
    given number of `days` offset to now (negative for words published
    in the past, positive for words that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Word.objects.create(word_text=word_text, added_date=time)


class WordIndexViewTests(TestCase):
    def test_no_words(self):
        """
        If no words exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("words:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No words are available.")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_past_word(self):
        """
        Words with a added_date in the past are displayed on the index page
        """
        create_word(word_text="Past word.", days=-30)
        response = self.client.get(reverse("words:index"))
        self.assertQuerysetEqual(
            response.context["object_list"], ["<Word: Past word.>"]
        )

    def test_future_word(self):
        """
        Words with an added_date in the future aren't displayed on the index page
        """
        create_word(word_text="Future word.", days=30)
        response = self.client.get(reverse("words:index"))
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_future_and_past_word(self):
        """
        Even if both past and future words exist, only past words
        are displayed.
        """
        create_word(word_text="Future word.", days=30)
        create_word(word_text="Past word.", days=-30)
        response = self.client.get(reverse("words:index"))
        self.assertQuerysetEqual(
            response.context["object_list"], ["<Word: Past word.>"]
        )

    def test_two_past_words(self):
        """
        The words index page may dispaly multiple words, sorted from the latest
        """
        create_word(word_text="Past word 1.", days=-10)
        create_word(word_text="Past word 2.", days=-30)
        response = self.client.get(reverse("words:index"))
        self.assertQuerysetEqual(
            response.context["object_list"],
            ["<Word: Past word 1.>", "<Word: Past word 2.>"],
        )
