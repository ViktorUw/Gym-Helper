import datetime

from django.test import TestCase
from django.urls import reverse

from completed_trainings.models import Completed_Training, CompletedExercise
from reg_log.models import User

from .models import Category, Exercises


def make_user(email):
    return User.objects.create_user(
        email=email, password="Trudne-Haslo-123", first_name="Jan", last_name="Nowak"
    )


class ExerciseProgressTests(TestCase):
    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.other = make_user("anna@test.pl")
        category = Category.objects.create(name="Plecy")
        self.exercise = Exercises.objects.create(name="Wiosłowanie", category=category)
        self.url = reverse("exPage", args=[self.exercise.pk])
        self.client.force_login(self.user)

    def log_set(self, user, weight, repetitions=8, date=None):
        training = Completed_Training.objects.create(user=user, training_name="Trening")
        if date:
            # date has auto_now_add, so it can only be changed after creating
            Completed_Training.objects.filter(pk=training.pk).update(date=date)
        CompletedExercise.objects.create(
            training=training, exercise=self.exercise, repetitions=repetitions, weight=weight
        )

    def test_no_sets_shows_empty_state(self):
        response = self.client.get(self.url)

        self.assertIsNone(response.context["best"])
        self.assertContains(response, "Nie masz jeszcze serii tego ćwiczenia")

    def test_record_is_heaviest_set(self):
        self.log_set(self.user, weight=40, repetitions=10)
        self.log_set(self.user, weight=50, repetitions=6)
        self.log_set(self.user, weight=45, repetitions=8)

        response = self.client.get(self.url)

        self.assertEqual(response.context["best"].weight, 50)
        self.assertEqual(response.context["sets_count"], 3)

    def test_other_users_sets_are_ignored(self):
        self.log_set(self.user, weight=40)
        self.log_set(self.other, weight=100)

        response = self.client.get(self.url)

        self.assertEqual(response.context["best"].weight, 40)
        self.assertEqual(response.context["sets_count"], 1)

    def test_chart_needs_two_days(self):
        self.log_set(self.user, weight=40, date=datetime.date(2026, 1, 5))
        self.assertIsNone(self.client.get(self.url).context["chart"])

        self.log_set(self.user, weight=45, date=datetime.date(2026, 1, 12))
        response = self.client.get(self.url)

        self.assertIsNotNone(response.context["chart"])
        self.assertEqual(response.context["days_count"], 2)
