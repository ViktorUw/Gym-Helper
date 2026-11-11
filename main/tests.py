from django.test import TestCase
from django.urls import reverse

from reg_log.models import User, UserWeight

PASSWORD = "Trudne-Haslo-123"


def make_user(email):
    return User.objects.create_user(
        email=email, password=PASSWORD, first_name="Jan", last_name="Nowak", age=25
    )


class LoginRequiredTests(TestCase):
    def test_pages_redirect_to_login(self):
        pages = [
            ("userPage", []),
            ("edit_account", []),
            ("change_password", []),
            ("add_weight", []),
            ("edit_weight", [1]),
            ("delete_weight", [1]),
        ]
        for name, args in pages:
            with self.subTest(page=name):
                url = reverse(name, args=args)
                response = self.client.get(url)

                self.assertRedirects(
                    response, f"{reverse('login')}?next={url}", fetch_redirect_response=False
                )


class EditAccountTests(TestCase):
    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.client.force_login(self.user)

    def edit(self, **data):
        fields = {"first_name": "Janusz", "last_name": "Kowalski", "email": "janusz@test.pl", "age": 30}
        fields.update(data)
        return self.client.post(reverse("edit_account"), fields)

    def test_form_shows_current_values(self):
        response = self.client.get(reverse("edit_account"))

        self.assertContains(response, 'value="jan@test.pl"')
        self.assertContains(response, 'value="25"')

    def test_edit_account(self):
        response = self.edit()

        self.assertRedirects(response, reverse("userPage"))
        self.user.refresh_from_db()
        self.assertEqual(
            (self.user.first_name, self.user.last_name, self.user.email, self.user.age),
            ("Janusz", "Kowalski", "janusz@test.pl", 30),
        )

    def test_can_log_in_with_new_email(self):
        self.edit()
        self.client.logout()

        response = self.client.post(
            reverse("login"), {"email": "janusz@test.pl", "password1": PASSWORD}
        )

        self.assertRedirects(response, reverse("mainPage"))

    def test_email_taken_by_other_user(self):
        make_user("anna@test.pl")

        response = self.edit(email="anna@test.pl")

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "jan@test.pl")

    def test_invalid_age_rejected(self):
        response = self.edit(age=5)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.age, 25)


class ChangePasswordTests(TestCase):
    NEW = "Nowe-Haslo-456"

    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.client.force_login(self.user)

    def change(self, old=PASSWORD, new1=NEW, new2=NEW):
        return self.client.post(
            reverse("change_password"),
            {"old_password": old, "new_password1": new1, "new_password2": new2},
        )

    def test_change_password(self):
        response = self.change()

        self.assertRedirects(response, reverse("userPage"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.NEW))

    def test_stays_logged_in_after_change(self):
        self.change()

        self.assertEqual(self.client.get(reverse("userPage")).status_code, 200)

    def test_can_log_in_with_new_password_only(self):
        self.change()
        self.client.logout()

        old = self.client.post(reverse("login"), {"email": "jan@test.pl", "password1": PASSWORD})
        new = self.client.post(reverse("login"), {"email": "jan@test.pl", "password1": self.NEW})

        self.assertEqual(old.status_code, 200)
        self.assertRedirects(new, reverse("mainPage"))

    def test_wrong_old_password_rejected(self):
        response = self.change(old="zle-haslo")

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))

    def test_new_passwords_must_match(self):
        response = self.change(new2="Inne-Haslo-789")

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))


class WeightTests(TestCase):
    def setUp(self):
        self.user = make_user("jan@test.pl")
        self.other = make_user("anna@test.pl")
        self.measurement = UserWeight.objects.create(user=self.user, weight=80)
        self.client.force_login(self.user)

    def test_profile_lists_measurements(self):
        response = self.client.get(reverse("userPage"))

        self.assertEqual(response.context["weight_history"], [self.measurement])
        self.assertContains(response, reverse("edit_weight", args=[self.measurement.pk]))

    def test_add_weight(self):
        response = self.client.post(reverse("add_weight"), {"weight": 79.5})

        self.assertRedirects(response, reverse("userPage"))
        self.assertEqual(UserWeight.objects.filter(user=self.user).count(), 2)

    def test_add_invalid_weight_rejected(self):
        response = self.client.post(reverse("add_weight"), {"weight": 555})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserWeight.objects.filter(user=self.user).count(), 1)

    def test_edit_weight(self):
        response = self.client.post(
            reverse("edit_weight", args=[self.measurement.pk]), {"weight": 81}
        )

        self.assertRedirects(response, reverse("userPage"))
        self.measurement.refresh_from_db()
        self.assertEqual(self.measurement.weight, 81)

    def test_delete_weight(self):
        response = self.client.post(reverse("delete_weight", args=[self.measurement.pk]))

        self.assertRedirects(response, reverse("userPage"))
        self.assertFalse(UserWeight.objects.exists())

    def test_delete_weight_needs_post(self):
        response = self.client.get(reverse("delete_weight", args=[self.measurement.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(UserWeight.objects.exists())

    def test_cannot_touch_other_users_weight(self):
        self.client.force_login(self.other)

        edit = self.client.post(reverse("edit_weight", args=[self.measurement.pk]), {"weight": 99})
        delete = self.client.post(reverse("delete_weight", args=[self.measurement.pk]))

        self.assertEqual(edit.status_code, 404)
        self.assertEqual(delete.status_code, 404)
        self.measurement.refresh_from_db()
        self.assertEqual(self.measurement.weight, 80)
