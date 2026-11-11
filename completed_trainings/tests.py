from django.test import TestCase
from django.urls import reverse

from exercises.models import Category, Exercises
from reg_log.models import User
from training_plans.models import CustomPlans, TrainingPlans

from .models import Completed_Training, CompletedExercise


def make_user(email):
    return User.objects.create_user(
        email=email, password="Trudne-Haslo-123", first_name="Jan", last_name="Nowak"
    )


class TrainingTestCase(TestCase):
    """Shared data: two users, one exercise, a ready plan, a custom plan, one training."""

    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.other = make_user("anna@test.pl")

        category = Category.objects.create(name="Plecy")
        self.exercise = Exercises.objects.create(name="Wiosłowanie", category=category)

        self.ready_plan = TrainingPlans.objects.create(name="FB Poniedziałek")
        self.ready_plan.exercises.add(self.exercise)

        self.custom_plan = CustomPlans.objects.create(name="Mój plan")
        self.custom_plan.user.add(self.user)
        self.custom_plan.exercises.add(self.exercise)

        self.training = Completed_Training.objects.create(
            user=self.user, training_name="Poniedziałek", training_plan=self.ready_plan
        )
        self.client.force_login(self.user)


class LoginRequiredTests(TestCase):
    def test_pages_redirect_to_login(self):
        for name in ["trainingsPage", "add_weightPage", "choseTrainingPlanPage"]:
            with self.subTest(page=name):
                url = reverse(name)
                response = self.client.get(url)

                self.assertRedirects(response, f"{reverse('login')}?next={url}")


class SeriesTests(TrainingTestCase):
    def add_series(self, repetitions=10, weight=40):
        return self.client.post(
            reverse("do_seriesPage", args=[self.training.pk]),
            {"exercise": self.exercise.pk, "repetitions": repetitions, "weight": weight},
        )

    def test_add_series(self):
        response = self.add_series()

        self.assertRedirects(
            response, reverse("ct_create_trainingsPage", args=[self.training.pk])
        )
        self.assertEqual(CompletedExercise.objects.count(), 1)

    def test_zero_repetitions_rejected(self):
        response = self.add_series(repetitions=0)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CompletedExercise.objects.exists())


class OtherUsersDataTests(TrainingTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.other)

    def test_cannot_open_other_users_training(self):
        url = reverse("ct_create_trainingsPage", args=[self.training.pk])

        self.assertEqual(self.client.get(url).status_code, 404)

    def test_cannot_add_series_to_other_users_training(self):
        response = self.client.post(
            reverse("do_seriesPage", args=[self.training.pk]),
            {"exercise": self.exercise.pk, "repetitions": 10, "weight": 40},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(CompletedExercise.objects.exists())


class DeletePlanTests(TrainingTestCase):
    def test_deleting_plan_keeps_trainings(self):
        training = Completed_Training.objects.create(
            user=self.user, training_name="Własny", custom_plan=self.custom_plan
        )
        CompletedExercise.objects.create(
            training=training, exercise=self.exercise, repetitions=10, weight=40
        )

        self.client.post(reverse("delete_plan", args=[self.custom_plan.pk]))

        training.refresh_from_db()
        self.assertIsNone(training.custom_plan)
        self.assertEqual(CompletedExercise.objects.filter(training=training).count(), 1)


class EditDeleteSeriesTests(TrainingTestCase):
    def setUp(self):
        super().setUp()
        self.series = CompletedExercise.objects.create(
            training=self.training, exercise=self.exercise, repetitions=10, weight=40
        )
        self.training_url = reverse("ct_create_trainingsPage", args=[self.training.pk])

    def edit(self, repetitions=12, weight=45):
        return self.client.post(
            reverse("edit_series", args=[self.series.pk]),
            {"exercise": self.exercise.pk, "repetitions": repetitions, "weight": weight},
        )

    def test_edit_series(self):
        response = self.edit()

        self.assertRedirects(response, self.training_url)
        self.series.refresh_from_db()
        self.assertEqual((self.series.repetitions, self.series.weight), (12, 45))

    def test_edit_rejects_invalid_values(self):
        response = self.edit(repetitions=0)

        self.assertEqual(response.status_code, 200)
        self.series.refresh_from_db()
        self.assertEqual(self.series.repetitions, 10)

    def test_delete_series(self):
        response = self.client.post(reverse("delete_series", args=[self.series.pk]))

        self.assertRedirects(response, self.training_url)
        self.assertFalse(CompletedExercise.objects.exists())

    def test_delete_series_needs_post(self):
        response = self.client.get(reverse("delete_series", args=[self.series.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(CompletedExercise.objects.exists())

    def test_cannot_edit_or_delete_other_users_series(self):
        self.client.force_login(self.other)

        self.assertEqual(self.edit().status_code, 404)
        response = self.client.post(reverse("delete_series", args=[self.series.pk]))
        self.assertEqual(response.status_code, 404)

        self.series.refresh_from_db()
        self.assertEqual(self.series.repetitions, 10)
