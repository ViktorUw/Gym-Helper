from rest_framework.test import APITestCase

from exercises.models import Category, Exercises
from reg_log.models import User

from .models import CustomPlans, TrainingPlans


def make_user(email):
    return User.objects.create_user(
        email=email, password="Trudne-Haslo-123", first_name="Jan", last_name="Nowak"
    )


class PlanApiTests(APITestCase):
    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.other = make_user("anna@test.pl")
        category = Category.objects.create(name="Plecy")
        self.exercise = Exercises.objects.create(name="Wiosłowanie", category=category)

        self.ready_plan = TrainingPlans.objects.create(name="FB Poniedziałek")
        self.ready_plan.exercises.add(self.exercise)
        self.own_plan = CustomPlans.objects.create(name="Mój plan")
        self.own_plan.user.add(self.user)
        self.other_plan = CustomPlans.objects.create(name="Plan Anny")
        self.other_plan.user.add(self.other)

        self.client.force_authenticate(self.user)

    def test_ready_plans_list_exercise_ids(self):
        response = self.client.get("/api/plans/")

        self.assertEqual(response.data[0]["name"], "FB Poniedziałek")
        self.assertEqual(response.data[0]["exercises"], [self.exercise.pk])

    def test_custom_plans_only_own(self):
        response = self.client.get("/api/custom-plans/")

        self.assertEqual([plan["name"] for plan in response.data], ["Mój plan"])

    def test_other_users_custom_plan_404(self):
        response = self.client.get(f"/api/custom-plans/{self.other_plan.pk}/")

        self.assertEqual(response.status_code, 404)
