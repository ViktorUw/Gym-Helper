from rest_framework.test import APITestCase

from reg_log.models import User

from .models import Category, Exercises


class ExerciseApiTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="Plecy")
        self.exercise = Exercises.objects.create(name="Wiosłowanie", category=category)
        self.user = User.objects.create_user(
            email="jan@test.pl", password="Trudne-Haslo-123", first_name="Jan", last_name="Nowak"
        )

    def test_requires_login(self):
        response = self.client.get("/api/exercises/")

        self.assertEqual(response.status_code, 403)

    def test_list_exercises(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/exercises/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Wiosłowanie")
        self.assertEqual(response.data[0]["category"], "Plecy")

    def test_exercise_detail(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(f"/api/exercises/{self.exercise.pk}/")

        self.assertEqual(response.data["id"], self.exercise.pk)

    def test_read_only(self):
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/exercises/", {"name": "Nowe"})

        self.assertEqual(response.status_code, 405)
