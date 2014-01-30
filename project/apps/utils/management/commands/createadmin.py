from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create a new superuser without prompting the user for input"

    def handle(self, *args, **options):
        user = User(username="__ADMIN_USERNAME__", email="__ADMIN_USERNAME__@local.com",
                    is_superuser=True, is_staff=True)
        user.set_password("__ADMIN_PASSWORD__")
        user.save()

        self.stdout.write("Created admin: __ADMIN_USERNAME__\n")
