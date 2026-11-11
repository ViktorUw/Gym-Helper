from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from exercises.models import Category, Exercises
from reg_log.models import User
from training_plans.models import CustomPlans, TrainingPlans

from .models import Completed_Training, CompletedExercise

PASSWORD = "Trudne-Haslo-123"


def make_user(email):
    return User.objects.create_user(
        email=email, password=PASSWORD, first_name="Jan", last_name="Nowak"
    )


class ApiTestCase(APITestCase):
    """Shared data: two users, a plan with one exercise, one training of self.user."""

    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.other = make_user("anna@test.pl")
        category = Category.objects.create(name="Plecy")
        self.exercise = Exercises.objects.create(name="Wiosłowanie", category=category)
        self.not_in_plan = Exercises.objects.create(name="Przysiad", category=category)

        self.plan = TrainingPlans.objects.create(name="FB Poniedziałek")
        self.plan.exercises.add(self.exercise)

        self.training = Completed_Training.objects.create(
            user=self.user, training_name="Poniedziałek", training_plan=self.plan
        )
        self.client.force_authenticate(self.user)


class TrainingApiTests(ApiTestCase):
    def test_list_only_own_trainings(self):
        Completed_Training.objects.create(user=self.other, training_name="Anny", training_plan=self.plan)

        response = self.client.get("/api/trainings/")

        self.assertEqual([t["training_name"] for t in response.data], ["Poniedziałek"])

    def test_create_training(self):
        response = self.client.post(
            "/api/trainings/", {"training_name": "Środa", "training_plan": self.plan.pk}
        )

        self.assertEqual(response.status_code, 201)
        training = Completed_Training.objects.get(training_name="Środa")
        self.assertEqual(training.user, self.user)

    def test_create_needs_exactly_one_plan(self):
        custom = CustomPlans.objects.create(name="Mój")
        custom.user.add(self.user)

        no_plan = self.client.post("/api/trainings/", {"training_name": "Bez planu"})
        both = self.client.post(
            "/api/trainings/",
            {"training_name": "Oba", "training_plan": self.plan.pk, "custom_plan": custom.pk},
        )

        self.assertEqual(no_plan.status_code, 400)
        self.assertEqual(both.status_code, 400)

    def test_cannot_use_other_users_custom_plan(self):
        other_plan = CustomPlans.objects.create(name="Plan Anny")
        other_plan.user.add(self.other)

        response = self.client.post(
            "/api/trainings/", {"training_name": "X", "custom_plan": other_plan.pk}
        )

        self.assertEqual(response.status_code, 400)

    def test_detail_has_sets_and_summary(self):
        CompletedExercise.objects.create(
            training=self.training, exercise=self.exercise, repetitions=10, weight=40
        )

        response = self.client.get(f"/api/trainings/{self.training.pk}/")

        self.assertEqual(len(response.data["sets"]), 1)
        self.assertEqual(response.data["summary"]["volume"], 400)

    def test_other_users_training_404(self):
        self.client.force_authenticate(self.other)

        response = self.client.get(f"/api/trainings/{self.training.pk}/")
        delete = self.client.delete(f"/api/trainings/{self.training.pk}/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(delete.status_code, 404)
        self.assertTrue(Completed_Training.objects.filter(pk=self.training.pk).exists())


class SetApiTests(ApiTestCase):
    def add_set(self, **data):
        fields = {"training": self.training.pk, "exercise": self.exercise.pk, "repetitions": 10, "weight": 40}
        fields.update(data)
        return self.client.post("/api/sets/", fields)

    def test_add_set(self):
        response = self.add_set()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(CompletedExercise.objects.get().training, self.training)

    def test_invalid_numbers_rejected(self):
        self.assertEqual(self.add_set(repetitions=0).status_code, 400)
        self.assertEqual(self.add_set(weight=-1).status_code, 400)
        self.assertFalse(CompletedExercise.objects.exists())

    def test_exercise_must_be_in_plan(self):
        response = self.add_set(exercise=self.not_in_plan.pk)

        self.assertEqual(response.status_code, 400)
        self.assertIn("exercise", response.data)

    def test_cannot_add_set_to_other_users_training(self):
        self.client.force_authenticate(self.other)

        response = self.add_set()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(CompletedExercise.objects.exists())

    def test_cannot_edit_or_delete_other_users_set(self):
        set_id = self.add_set().data["id"]
        self.client.force_authenticate(self.other)

        edit = self.client.patch(f"/api/sets/{set_id}/", {"weight": 99})
        delete = self.client.delete(f"/api/sets/{set_id}/")

        self.assertEqual(edit.status_code, 404)
        self.assertEqual(delete.status_code, 404)
        self.assertEqual(CompletedExercise.objects.get().weight, 40)

    def test_edit_and_delete_set(self):
        set_id = self.add_set().data["id"]

        edit = self.client.patch(f"/api/sets/{set_id}/", {"weight": 45})
        self.assertEqual(edit.data["weight"], 45)

        delete = self.client.delete(f"/api/sets/{set_id}/")
        self.assertEqual(delete.status_code, 204)
        self.assertFalse(CompletedExercise.objects.exists())

    def test_filter_by_training(self):
        self.add_set()
        second = Completed_Training.objects.create(user=self.user, training_name="Wtorek", training_plan=self.plan)
        self.add_set(training=second.pk)

        response = self.client.get(f"/api/sets/?training={second.pk}")

        self.assertEqual([s["training"] for s in response.data], [second.pk])


class TokenApiTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(None)  # these tests log in with a token instead

    def test_get_token_with_email_and_password(self):
        response = self.client.post("/api/token/", {"username": "jan@test.pl", "password": PASSWORD})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["token"], Token.objects.get(user=self.user).key)

    def test_wrong_password_gets_no_token(self):
        response = self.client.post("/api/token/", {"username": "jan@test.pl", "password": "zle"})

        self.assertEqual(response.status_code, 400)

    def test_token_gives_access(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.get("/api/trainings/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
