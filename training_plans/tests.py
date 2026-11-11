from django.test import TestCase
from django.urls import reverse

from exercises.models import Category, Exercises
from reg_log.models import User

from .models import CustomPlans, TrainingPlans


def make_user(email):
    return User.objects.create_user(
        email=email, password="Trudne-Haslo-123", first_name="Jan", last_name="Nowak"
    )


class PlanTestCase(TestCase):
    """Shared data: two users, one exercise and a custom plan owned by self.user."""

    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.other = make_user("anna@test.pl")

        category = Category.objects.create(name="Plecy")
        self.exercise = Exercises.objects.create(name="Wiosłowanie", category=category)

        self.plan = CustomPlans.objects.create(name="Mój plan")
        self.plan.user.add(self.user)
        self.plan.exercises.add(self.exercise)

        self.client.force_login(self.user)

    def plan_exists(self):
        return CustomPlans.objects.filter(pk=self.plan.pk).exists()


class LoginRequiredTests(TestCase):
    def test_pages_redirect_to_login(self):
        for name in ["trainingPlansPage", "create_plan"]:
            with self.subTest(page=name):
                url = reverse(name)
                response = self.client.get(url)

                self.assertRedirects(response, f"{reverse('login')}?next={url}")


class CreatePlanTests(PlanTestCase):
    def test_create_plan(self):
        response = self.client.post(
            reverse("create_plan"),
            {"name": "Nogi", "description": "Dzień nóg", "exercises": [self.exercise.pk]},
        )

        self.assertRedirects(response, reverse("trainingPlansPage"))
        plan = CustomPlans.objects.get(name="Nogi")
        self.assertIn(self.user, plan.user.all())
        self.assertIn(self.exercise, plan.exercises.all())

    def test_plan_without_exercises_rejected(self):
        response = self.client.post(
            reverse("create_plan"), {"name": "Pusty", "description": "Bez ćwiczeń"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomPlans.objects.filter(name="Pusty").exists())


class OtherUsersPlanTests(PlanTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.other)

    def test_cannot_open_other_users_plan(self):
        response = self.client.get(reverse("customPlanPage", args=[self.plan.pk]))

        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_other_users_plan(self):
        response = self.client.post(reverse("delete_plan", args=[self.plan.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(self.plan_exists())

    def test_other_users_plan_not_listed(self):
        response = self.client.get(reverse("trainingPlansPage"))

        self.assertNotContains(response, "Mój plan")


class DeletePlanTests(PlanTestCase):
    def test_delete_own_plan(self):
        response = self.client.post(reverse("delete_plan", args=[self.plan.pk]))

        self.assertRedirects(response, reverse("trainingPlansPage"))
        self.assertFalse(self.plan_exists())

    def test_delete_plan_needs_post(self):
        response = self.client.get(reverse("delete_plan", args=[self.plan.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(self.plan_exists())


class ReadyPlanTests(PlanTestCase):
    def test_open_ready_plan(self):
        plan = TrainingPlans.objects.create(name="FB Poniedziałek")
        plan.exercises.add(self.exercise)

        response = self.client.get(reverse("trainingPlanPage", args=[plan.pk]))

        self.assertContains(response, "FB Poniedziałek")
        self.assertContains(response, "Wiosłowanie")

    def test_missing_plan_returns_404(self):
        response = self.client.get(reverse("trainingPlanPage", args=[9999]))

        self.assertEqual(response.status_code, 404)


class EditPlanTests(PlanTestCase):
    def setUp(self):
        super().setUp()
        self.second_exercise = Exercises.objects.create(
            name="Podciąganie", category=self.exercise.category
        )

    def edit(self, **data):
        fields = {"name": "Nowa nazwa", "description": "Nowy opis", "exercises": [self.second_exercise.pk]}
        fields.update(data)
        return self.client.post(reverse("edit_plan", args=[self.plan.pk]), fields)

    def test_edit_form_shows_current_values(self):
        response = self.client.get(reverse("edit_plan", args=[self.plan.pk]))

        self.assertContains(response, 'value="Mój plan"')
        self.assertEqual(list(response.context["form"]["exercises"].value()), [self.exercise.pk])

    def test_edit_plan(self):
        response = self.edit()

        self.assertRedirects(response, reverse("customPlanPage", args=[self.plan.pk]))
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Nowa nazwa")
        self.assertEqual(list(self.plan.exercises.all()), [self.second_exercise])
        self.assertIn(self.user, self.plan.user.all())

    def test_edit_without_exercises_rejected(self):
        response = self.edit(exercises=[])

        self.assertEqual(response.status_code, 200)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Mój plan")

    def test_cannot_edit_other_users_plan(self):
        self.client.force_login(self.other)

        self.assertEqual(self.client.get(reverse("edit_plan", args=[self.plan.pk])).status_code, 404)
        self.assertEqual(self.edit().status_code, 404)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Mój plan")
