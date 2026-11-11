from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from exercises.models import Category


class Command(BaseCommand):
    help = "Load exercises, categories and ready-made plans, but only into an empty database."

    def handle(self, *args, **options):
        # Safe to run on every start: loading the fixture twice would duplicate nothing
        # (it has fixed ids), but it would undo changes made in the admin
        if Category.objects.exists():
            self.stdout.write("Exercises already loaded, skipping.")
            return
        call_command("loaddata", settings.BASE_DIR / "fixtures" / "initial_data.json")
