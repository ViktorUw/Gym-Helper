from django.test import TestCase
from django.urls import reverse

from .models import User

PASSWORD = "Trudne-Haslo-123"


class RegistrationTests(TestCase):
    def register(self, email, password2=PASSWORD):
        return self.client.post(
            reverse("registration"),
            {
                "first_name": "Jan",
                "last_name": "Novak",
                "age": 25,
                "email": email,
                "password1": PASSWORD,
                "password2": password2,
            },
        )

    def test_two_users_can_register(self):
        self.register("jan@test.pl")
        response = self.register("anna@test.pl")
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(User.objects.count(), 2)

    def test_different_passwords_show_error(self):
        response = self.register("jan@test.pl", password2="Inne-Haslo-999")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response.context["form"], "password2", "Hasła w obu polach nie są zgodne."
        )


class LoginTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            email="jan@test.pl",
            password=PASSWORD,
            first_name="Jan",
            last_name="Nowakowski",
        )

    def login(self, password=PASSWORD, next_url=""):
        return self.client.post(
            reverse("login"),
            {"email": "jan@test.pl", "password1": password, "next": next_url},
        )

    def test_login_goes_to_main_page(self):
        self.assertRedirects(self.login(), reverse("mainPage"))

    def test_login_returns_to_next_page(self):
        self.assertRedirects(self.login(next_url="/training/"), "/training/")

    def test_login_ignores_external_next(self):
        self.assertRedirects(
            self.login(next_url="https://google.com"), reverse("mainPage")
        )

    def test_wrong_password_does_not_log_in(self):
        response = self.login(password="zle-haslo")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class LogoutTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email="jan@test.pl",
            password=PASSWORD,
            first_name="Jan",
            last_name="Nowakowski",
        )
        self.client.force_login(user)

    def test_get_does_not_log_out(self):
        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

    def test_post_logs_out(self):
        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
